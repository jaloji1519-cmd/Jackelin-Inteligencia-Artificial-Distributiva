"""Pestaña de semaforización nacional (demostración local)."""
import streamlit as st

from semaforizacion import (
    DEPARTAMENTOS, ETIQUETAS, ICONOS, contar, estados_iniciales, siguiente, simular,
)


def render():
    st.subheader("Semaforización nacional")
    st.caption("Monitoreo de demostración: los estados se generan localmente, "
               "sin datos oficiales ni sensores reales.")
    estados = st.session_state.estados
    conteo = contar(estados)

    columnas = st.columns(3)
    columnas[0].metric("🟢 Estable", conteo["verde"])
    columnas[1].metric("🟡 En observación", conteo["amarillo"])
    columnas[2].metric("🔴 Crítico", conteo["rojo"])

    izquierda, centro, _ = st.columns([1, 1, 3])
    if izquierda.button("Simular actualización"):
        st.session_state.estados = simular(estados)
        st.rerun()
    if centro.button("Reiniciar todo"):
        st.session_state.estados = estados_iniciales()
        st.rerun()

    st.markdown("Pulsa un territorio para cambiar su estado manualmente.")
    rejilla = st.columns(4)
    for indice, nombre in enumerate(DEPARTAMENTOS):
        with rejilla[indice % 4]:
            estado = estados[nombre]
            if st.button(ICONOS[estado] + " " + nombre,
                         key="territorio_" + nombre,
                         help=ETIQUETAS[estado]):
                st.session_state.estados[nombre] = siguiente(estado)
                st.rerun()
