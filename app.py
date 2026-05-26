import streamlit as st

st.set_page_config(
    page_title="Validador de patrones con automatas",
    layout="wide",
)

logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
with logo_col2:
    st.image("UQ.png", width=180)

st.markdown(
    """
# Documentación Técnica: Sistema de Validación y Extracción de Patrones Basado en Máquinas de Estados Finitos (FSM)

Juan Manuel Amador Roa

Valeria Florez Paz

Presentado a: Ana María Tamayo

Universidad del Quindío  
Facultad de Ingeniería  
Programa Ingenieria de Sistemas y Computación  
Teoría de lenguajes formales  
Armenia- 2026
"""
)

st.divider()

st.title("Validador de patrones con automatas finitos")

st.markdown(
    """
### Proyecto: Busqueda y validacion de patrones en textos y sistemas interactivos

Esta aplicacion usa Streamlit para exponer un motor de validacion manual basado en
automatas finitos deterministas. El sistema evita por completo el uso de librerias
de expresiones regulares y permite analizar multiples tipos de patrones en texto
y en formularios interactivos.

Use el menu lateral para acceder a los modulos de analisis de textos y validacion
de formularios.
"""
)
