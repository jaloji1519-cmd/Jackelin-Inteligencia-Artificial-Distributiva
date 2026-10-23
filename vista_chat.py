"""Pestaña de IA distributiva: conversación con los agentes."""
import streamlit as st

from agentes import user_message


def _mostrar(mensaje, indice, coordinador):
    """Dibuja un mensaje y permite generar su voz bajo demanda."""
    with st.chat_message("assistant" if mensaje.get("rol") == "asistente" else "user"):
        if mensaje.get("error"):
            st.error(mensaje["texto"])
            return
        st.markdown(mensaje["texto"])
        if mensaje.get("agentes"):
            st.caption("Agentes que intervinieron: " + ", ".join(mensaje["agentes"]))
        if mensaje.get("imagen"):
            st.image(mensaje["imagen"], caption="Imagen generada por IA")
        for aviso in mensaje.get("avisos", []):
            st.warning(aviso)
        if mensaje.get("rol") == "asistente" and not mensaje.get("audio"):
            if st.button("🔊 Generar la voz de esta respuesta", key="voz_" + str(indice),
                         disabled=coordinador is None):
                try:
                    with st.spinner("El agente de voz está sintetizando..."):
                        mensaje["audio"] = coordinador.agente_voz.sintetizar(mensaje["texto"])
                except Exception as error:
                    st.warning(user_message(error))
        if mensaje.get("audio"):
            st.audio(mensaje["audio"], format="audio/mpeg")
            if len(mensaje["texto"]) > 4096:
                st.caption("El audio lee los primeros 4096 caracteres.")


def render(coordinador, contexto):
    if coordinador is None:
        st.info("Configura tu clave API de OpenAI en la barra lateral o en el archivo "
                ".env para activar los agentes de texto, voz e imagen.")
    elif not st.session_state.mensajes:
        st.caption("El agente de semaforización ya aporta el estado nacional como contexto. "
                   "Prueba: ¿cómo está el monitoreo nacional y qué recomendaciones darías?")

    for indice, mensaje in enumerate(st.session_state.mensajes):
        _mostrar(mensaje, indice, coordinador)

    pregunta = st.chat_input("Escribe tu consulta para la IAD...", max_chars=1000,
                             disabled=coordinador is None)
    if not pregunta or not pregunta.strip():
        return
    texto = pregunta.strip()
    st.session_state.mensajes.append({"rol": "usuario", "texto": texto})
    with st.chat_message("user"):
        st.markdown(texto)
    try:
        with st.spinner("El coordinador reparte el trabajo entre los agentes..."):
            salida = coordinador.responder(
                st.session_state.mensajes, contexto,
                st.session_state.voz, st.session_state.imagen)
    except Exception as error:
        aviso = user_message(error)
        st.session_state.mensajes.append(
            {"rol": "asistente", "texto": aviso, "error": True})
        with st.chat_message("assistant"):
            st.error(aviso)
        return
    registro = {
        "rol": "asistente",
        "texto": salida["texto"],
        "audio": salida["audio"],
        "imagen": salida["imagen"],
        "avisos": salida["avisos"],
        "agentes": salida["agentes"],
    }
    st.session_state.mensajes.append(registro)
    _mostrar(registro, len(st.session_state.mensajes) - 1, coordinador)
