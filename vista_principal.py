import base64
from pathlib import Path

import streamlit as st


def _img_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _render_cover(logo_base64: str) -> None:
    template_path = Path(__file__).with_name("vista_principal_template.html")
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("{{LOGO_BASE64}}", logo_base64)
    st.markdown(html, unsafe_allow_html=True)


logo_b64 = _img_base64("UQ.png")

st.markdown('<div class="vista-principal">', unsafe_allow_html=True)

_render_cover(logo_b64)

st.divider()

st.title("Validador de patrones")

st.markdown(
    """
## 1. Descripción general

Aplicación web en **Streamlit** para **extraer** y **validar** patrones (correos, teléfonos, fechas, URLs, placas y contraseñas).

## 2. Funcionalidades

- **Módulo A (Análisis de textos):** extrae patrones válidos desde texto o archivos `.txt`/`.log`.
- **Módulo B (Formularios):** valida en tiempo real campos típicos de un formulario.
- **Resumen y métricas:** tablas de resultados y conteos por estado/tipo.

## 3. Motores disponibles

- **FSM (sin regex):** validación manual con máquinas de estados finitos.
- **Regex (re):** validación alternativa usando expresiones regulares.

## 4. Navegación

Use el menú lateral para acceder a las secciones.
"""
)

st.markdown("</div>", unsafe_allow_html=True)
