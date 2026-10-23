"""Agentes especializados y coordinador de la IA distribuida.

Cada agente es independiente y hace una sola cosa. El coordinador reparte el
trabajo: el agente de texto produce la respuesta escrita y, a partir de ella,
los agentes de voz e imagen trabajan en paralelo. El agente de semaforización
aporta el estado nacional como contexto y no necesita proveedor externo.
"""
import base64
import json
import os
from concurrent.futures import ThreadPoolExecutor

from openai import (
    APIConnectionError, APIStatusError, AuthenticationError, OpenAI,
    PermissionDeniedError, RateLimitError,
)

from semaforizacion import resumen_texto

ESQUEMA_RESPUESTA = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "imagen": {"type": ["string", "null"]},
    },
    "required": ["text", "imagen"],
    "additionalProperties": False,
}

ROLES = {"usuario": "user", "asistente": "assistant"}

SISTEMA = (
    "Eres JACKELIN, una Inteligencia Artificial Distribuida compuesta por agentes "
    "especializados: texto, voz, imagen y semaforización. Responde en español, de "
    "forma clara y útil, en un máximo de cuatro párrafos. No afirmes haber consultado "
    "internet ni datos oficiales en tiempo real; los estados de semaforización son de "
    "demostración. "
)


class AgenteTexto:
    """Agente de lenguaje: redacta la respuesta y una descripción visual opcional."""

    nombre = "texto"

    def __init__(self, cliente, modelo):
        self.cliente = cliente
        self.modelo = modelo

    def responder(self, historial, contexto, permitir_imagen):
        sistema = SISTEMA
        if contexto:
            sistema += "Contexto del agente de semaforización: " + contexto + ". "
        if permitir_imagen:
            sistema += (
                "Si una ilustración ayuda a explicar, devuelve en imagen una descripción "
                "visual detallada; si no, devuelve null. No prometas una imagen ya creada."
            )
        else:
            sistema += "El agente de imagen está apagado: imagen debe ser null."
        mensajes = [{"role": "system", "content": sistema}]
        mensajes.extend(
            {"role": ROLES.get(mensaje.get("rol"), "user"), "content": mensaje["texto"]}
            for mensaje in historial[-12:] if not mensaje.get("error")
        )
        respuesta = self.cliente.chat.completions.create(
            model=self.modelo,
            messages=mensajes,
            max_tokens=1600,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "respuesta_jackelin", "strict": True,
                    "schema": ESQUEMA_RESPUESTA,
                },
            },
        )
        opcion = respuesta.choices[0]
        if opcion.finish_reason == "length":
            raise ValueError("La respuesta superó el límite. Intenta una pregunta más corta.")
        if opcion.message.refusal:
            raise ValueError("El proveedor no puede responder esta solicitud. Reformúlala.")
        datos = json.loads(opcion.message.content or "{}")
        texto = (datos.get("text") or "").strip()
        if not texto:
            raise ValueError("El agente de texto no devolvió una respuesta válida.")
        return {
            "texto": texto,
            "descripcion": datos.get("imagen") if permitir_imagen else None,
        }


class AgenteVoz:
    """Agente de voz: convierte la respuesta escrita en audio MP3."""

    nombre = "voz"

    def __init__(self, cliente, modelo, voz):
        self.cliente = cliente
        self.modelo = modelo
        self.voz = voz

    def sintetizar(self, texto):
        audio = self.cliente.audio.speech.create(
            model=self.modelo,
            voice=self.voz,
            input=texto[:4096],
            response_format="mp3",
        )
        return audio.read()


class AgenteImagen:
    """Agente de imagen: dibuja una ilustración PNG a partir de la descripción."""

    nombre = "imagen"

    def __init__(self, cliente, modelo):
        self.cliente = cliente
        self.modelo = modelo

    def dibujar(self, descripcion):
        respuesta = self.cliente.images.generate(
            model=self.modelo,
            prompt=descripcion[:2000],
            size="1024x1024",
            quality="low",
            n=1,
        )
        if not respuesta.data or not respuesta.data[0].b64_json:
            raise ValueError("El agente de imagen no devolvió una imagen válida.")
        return base64.b64decode(respuesta.data[0].b64_json, validate=True)


class AgenteSemaforizacion:
    """Agente local: resume el estado nacional y lo entrega como contexto."""

    nombre = "semaforización"

    def contexto(self, estados):
        return resumen_texto(estados)


class CoordinadorIAD:
    """Orquesta los agentes: fan-out del trabajo y fan-in de los resultados."""

    def __init__(self, clave_api):
        if not clave_api:
            raise ValueError("Falta la clave API.")
        self.cliente = OpenAI(api_key=clave_api, timeout=180.0, max_retries=1)
        self.agente_texto = AgenteTexto(
            self.cliente, os.getenv("TEXT_MODEL", "gpt-4o-mini"))
        self.agente_voz = AgenteVoz(
            self.cliente, os.getenv("VOICE_MODEL", "tts-1"), os.getenv("VOICE_NAME", "nova"))
        self.agente_imagen = AgenteImagen(
            self.cliente, os.getenv("IMAGE_MODEL", "gpt-image-1"))
        self.agente_semaforizacion = AgenteSemaforizacion()

    def responder(self, historial, contexto, con_voz, con_imagen):
        """Fase 1: agente de texto. Fase 2: voz e imagen en paralelo."""
        salida = self.agente_texto.responder(historial, contexto, con_imagen)
        resultado = {
            "texto": salida["texto"],
            "audio": None,
            "imagen": None,
            "avisos": [],
            "agentes": [self.agente_texto.nombre],
        }
        tareas = {}
        with ThreadPoolExecutor(max_workers=2) as ejecutor:
            if con_voz:
                tareas["voz"] = ejecutor.submit(
                    self.agente_voz.sintetizar, salida["texto"])
            if con_imagen and salida["descripcion"]:
                tareas["imagen"] = ejecutor.submit(
                    self.agente_imagen.dibujar, salida["descripcion"])
            for nombre, tarea in tareas.items():
                try:
                    if nombre == "voz":
                        resultado["audio"] = tarea.result()
                    else:
                        resultado["imagen"] = tarea.result()
                    resultado["agentes"].append(nombre)
                except Exception as error:
                    resultado["avisos"].append(nombre.capitalize() + ": " + user_message(error))
        return resultado


def user_message(error):
    """Mensajes comprensibles, sin exponer claves ni respuestas internas."""
    if isinstance(error, AuthenticationError):
        return "La clave API no es válida. Revisa tu archivo .env o la barra lateral."
    if isinstance(error, PermissionDeniedError):
        return "La cuenta no tiene acceso a este modelo. Revisa sus permisos o verificación."
    if isinstance(error, RateLimitError):
        return "Se alcanzó el límite o no hay saldo de API. Revisa tu cuenta y vuelve a intentar."
    if isinstance(error, APIConnectionError):
        return "No se pudo conectar con la API. Revisa internet e inténtalo otra vez."
    if isinstance(error, APIStatusError):
        return "La API rechazó la solicitud. Revisa disponibilidad y compatibilidad del modelo."
    if isinstance(error, json.JSONDecodeError):
        return "La respuesta no tuvo el formato esperado. Inténtalo otra vez."
    if isinstance(error, ValueError):
        return str(error)
    return "No fue posible completar la operación. Revisa tu configuración e inténtalo otra vez."
