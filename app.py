import base64

import streamlit as st

st.set_page_config(
    page_title="Validador de patrones con automatas",
    layout="wide",
)


def _img_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


logo_b64 = _img_base64("UQ.png")

st.markdown(
    """
<style>
/* Fondo "de escritorio" para resaltar la hoja blanca */
[data-testid="stAppViewContainer"] {
  background: #f3f4f6;
}

.cover-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 56px 72px;
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 10px;
  box-shadow: 0 18px 55px rgba(0,0,0,0.10);
}

.cover-center { text-align: center; }
.cover-title {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.25;
  margin-top: 24px;
  margin-bottom: 0;
}
.cover-block { margin-top: 34px; }
.cover-text { font-size: 18px; line-height: 1.6; }
.cover-muted { font-size: 17px; line-height: 1.6; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="cover-page">
  <div class="cover-center">
    <img src="data:image/png;base64,{logo_b64}" alt="Universidad del Quindío" style="width:180px; height:auto;" />

    <div class="cover-title">
      Documentación Técnica: Sistema de Validación y Extracción de Patrones Basado en Máquinas de Estados Finitos (FSM)
    </div>
  </div>

  <div class="cover-center cover-block cover-text">
    Juan Manuel Amador Roa<br><br>
    Valeria Florez Paz
  </div>

  <div class="cover-center cover-block cover-text">
    Presentado a: Ana María Tamayo
  </div>

  <div class="cover-center cover-block cover-muted">
    Universidad del Quindío<br>
    Facultad de Ingeniería<br>
    Programa Ingenieria de Sistemas y Computación<br>
    Teoría de lenguajes formales<br>
    Armenia- 2026
  </div>
</div>
""",
    unsafe_allow_html=True,
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
