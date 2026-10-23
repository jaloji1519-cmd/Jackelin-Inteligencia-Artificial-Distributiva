"""Semaforización nacional: modelo, simulación y resumen.

Demostración local: los estados se generan dentro del programa con reglas y
azar. No existe conexión con entidades oficiales, sensores ni datos reales.
"""
import random

DEPARTAMENTOS = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bogotá D.C.", "Bolívar",
    "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó",
    "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira",
    "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío",
    "Risaralda", "San Andrés y Providencia", "Santander", "Sucre", "Tolima",
    "Valle del Cauca", "Vaupés", "Vichada",
]

ESTADOS = ["verde", "amarillo", "rojo"]
PESOS = [0.6, 0.3, 0.1]
ETIQUETAS = {
    "verde": "Estable",
    "amarillo": "En observación",
    "rojo": "Crítico",
}
ICONOS = {
    "verde": "🟢",
    "amarillo": "🟡",
    "rojo": "🔴",
}


def estados_iniciales():
    """Todos los territorios inician estables."""
    return {nombre: "verde" for nombre in DEPARTAMENTOS}


def siguiente(estado):
    """Recorre el ciclo verde -> amarillo -> rojo -> verde."""
    return ESTADOS[(ESTADOS.index(estado) + 1) % len(ESTADOS)]


def contar(estados):
    """Cantidad de territorios por estado."""
    conteo = {estado: 0 for estado in ESTADOS}
    for valor in estados.values():
        if valor in conteo:
            conteo[valor] += 1
    return conteo


def simular(estados):
    """Actualización ponderada para la demostración."""
    return {
        nombre: random.choices(ESTADOS, weights=PESOS, k=1)[0]
        for nombre in estados
    }


def resumen_texto(estados):
    """Frase de contexto que consume el agente de texto."""
    conteo = contar(estados)
    return (
        "monitoreo de demostración: {verde} territorios estables, "
        "{amarillo} en observación y {rojo} en estado crítico"
    ).format(**conteo)
