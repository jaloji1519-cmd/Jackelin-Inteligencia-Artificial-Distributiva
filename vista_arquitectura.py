"""Pestaña del reporte de arquitectura de la IAD."""
import streamlit as st

from arquitectura import DIAGRAMA, INTRO, SECCIONES


def render():
    st.subheader("Arquitectura de la IA distribuida")
    st.markdown(INTRO)
    for seccion in SECCIONES:
        with st.expander(seccion["titulo"], expanded=False):
            st.markdown(seccion["detalle"])
    st.markdown("**Diagrama por capas**")
    st.code(DIAGRAMA, language=None)
