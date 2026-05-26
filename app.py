import streamlit as st

st.set_page_config(
    page_title="Validador de patrones",
    layout="wide",
)

pages = [
    st.Page("vista_principal.py", title="Vista principal"),
    st.Page("pages/1_analizador_texto.py", title="Análisis de textos"),
    st.Page("pages/2_formularios.py", title="Validación de formularios"),
]

pg = st.navigation(pages)
pg.run()
