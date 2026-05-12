import streamlit as st

st.set_page_config(
    page_title="Validador de patrones con automatas",
    layout="wide",
)

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
