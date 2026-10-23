"""Contenido del reporte de arquitectura de la IAD."""

INTRO = (
    "Sistema: JACKELIN · Objetivo: chat multimodal con IA distributiva y "
    "monitoreo nacional de demostración · Distribución: agentes especializados "
    "con un coordinador central · Recursos: nube híbrida y nodos en el borde · "
    "Restricciones: baja latencia, privacidad de datos y degradación elegante."
)

SECCIONES = [
    {
        "titulo": "1. Topología distribuida",
        "detalle": (
            "Un coordinador central recibe la consulta y la reparte entre agentes "
            "que pueden ejecutarse en nodos distintos: la nube aloja la orquestación "
            "y los modelos grandes, mientras la inferencia ligera (validaciones, "
            "formato y semaforización) puede vivir en el borde, cerca del dato. "
            "Esta entrega ejecuta todos los agentes en el mismo proceso, pero "
            "mantiene la separación de responsabilidades para poder distribuirlos."
        ),
    },
    {
        "titulo": "2. Agentes especializados",
        "detalle": (
            "Agente de texto: redacta la respuesta y decide si una ilustración ayuda. "
            "Agente de voz: convierte el texto en audio. Agente de imagen: dibuja la "
            "ilustración descrita. Agente de semaforización: resume el estado nacional "
            "y lo entrega como contexto. Cada agente tiene una sola tarea y puede "
            "escalarse o reemplazarse por separado sin romper a los demás."
        ),
    },
    {
        "titulo": "3. Comunicación y orquestación",
        "detalle": (
            "El coordinador hace fan-out (reparte el trabajo) y fan-in (combina los "
            "resultados). Los agentes intercambian datos en JSON, un contrato simple y "
            "verificable. En esta entrega la concurrencia se resuelve con hilos y un "
            "grupo de tareas; en producción ese mismo contrato se transporta con colas "
            "de mensajes, lo que permite reintentos y escalado horizontal."
        ),
    },
    {
        "titulo": "4. Privacidad y seguridad",
        "detalle": (
            "La clave del proveedor vive en el servidor (archivo .env excluido de Git) "
            "y nunca se expone al navegador. Solo se envían al proveedor los mensajes "
            "necesarios y un máximo de doce mensajes recientes de contexto. En la versión "
            "web, el acceso a los datos se controla por usuario, roles y reglas por "
            "registro; aquí el historial permanece en la sesión local."
        ),
    },
    {
        "titulo": "5. Latencia y cuellos de botella",
        "detalle": (
            "El agente de texto es el cuello de botella porque los demás dependen de él, "
            "así que se ejecuta primero y sin trabajo adicional. Voz e imagen se lanzan "
            "en paralelo sobre el texto ya obtenido. Si un agente opcional falla, el "
            "sistema degrada con elegancia: se conserva la respuesta escrita y se avisa "
            "al usuario. Se limitan tamaños de entrada y salida para acotar el costo."
        ),
    },
    {
        "titulo": "6. Alcance de esta demostración",
        "detalle": (
            "Se ejecuta localmente con una clave propia del usuario, sin base de datos, "
            "sin usuarios ni despliegue público. Los estados de semaforización se generan "
            "con reglas y azar dentro del programa: no provienen de entidades oficiales "
            "ni de sensores reales y no deben usarse para decisiones operativas."
        ),
    },
]

DIAGRAMA = (
    "+---------------------------------------------------------------------+\n"
    "|  Capa de presentación: navegador / Streamlit (servidor local)       |\n"
    "+---------------------------------------------------------------------+\n"
    "                                  |\n"
    "                                  v\n"
    "+---------------------------------------------------------------------+\n"
    "|  Capa de coordinación: CoordinadorIAD (orquestador central)         |\n"
    "|  fan-out -> agentes   |   fan-in -> respuesta combinada             |\n"
    "+---------------------------------------------------------------------+\n"
    "        |               |               |                |\n"
    "        v               v               v                v\n"
    "  +-----------+   +-----------+   +-----------+   +-----------------+\n"
    "  | Agente de |   | Agente de |   | Agente de |   | Agente de       |\n"
    "  | texto     |   | voz       |   | imagen    |   | semaforización  |\n"
    "  +-----------+   +-----------+   +-----------+   +-----------------+\n"
    "        |               |               |                |\n"
    "        v               v               v                v\n"
    "   Modelo de       Modelo de       Modelo de         Datos de\n"
    "   lenguaje        voz (TTS)       imagen            demostración\n"
    "        \\________________|________________/\n"
    "                                  v\n"
    "+---------------------------------------------------------------------+\n"
    "|  Capa de datos: sesión local (historial, estados y resultados)      |\n"
    "+---------------------------------------------------------------------+"
)
