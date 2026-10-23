"""JACKELIN · Inteligencia Artificial Distribuida (IAD).

Punto de entrada: cabecera, barra lateral del coordinador y tres pestañas.
La lógica vive en módulos independientes (agentes, semaforización, vistas).
"""
import os

import streamlit as st
from dotenv import load_dotenv

from agentes import CoordinadorIAD
from semaforizacion import contar, estados_iniciales, resumen_texto
from vista_arquitectura import render as render_arquitectura
from vista_chat import render as render_chat
from vista_semaforizacion import render as render_semaforizacion

load_dotenv()
st.set_page_config(page_title="JACKELIN · IA distributiva", page_icon="🧠", layout="wide")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "estados" not in st.session_state:
    st.session_state.estados = estados_iniciales()
if "voz" not in st.session_state:
    st.session_state.voz = False
if "imagen" not in st.session_state:
    st.session_state.imagen = True

with st.sidebar:
    st.header("Coordinador IAD")
    clave = st.text_input(
        "Clave API de OpenAI", type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Puedes configurarla en el archivo .env. No la compartas ni la subas a GitHub.",
    ).strip()
    st.session_state.voz = st.toggle("Agente de voz", value=st.session_state.voz)
    st.session_state.imagen = st.toggle("Agente de imagen", value=st.session_state.imagen)
    st.caption("Agentes: texto, voz, imagen y semaforización.")
    st.caption("Las llamadas a la API pueden tener costo. No se incluye una clave.")
    if st.button("Nueva conversación"):
        st.session_state.mensajes = []
        st.rerun()

coordinador = CoordinadorIAD(clave) if clave else None
conteo = contar(st.session_state.estados)
contexto = resumen_texto(st.session_state.estados)

st.title("JACKELIN")
st.caption("Inteligencia Artificial Distribuida · texto, voz, imagen y semaforización nacional")

pestanas = st.tabs(["IA Distributiva", "Semaforización Nacional", "Arquitectura IAD"])
with pestanas[0]:
    render_chat(coordinador, contexto)
with pestanas[1]:
    render_semaforizacion()
with pestanas[2]:
    render_arquitectura()
