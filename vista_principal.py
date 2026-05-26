import base64

import streamlit as st


def _img_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


logo_b64 = _img_base64("UQ.png")

st.markdown(
    """
<style>
/* Estilos SOLO para la vista principal (scoped por clase) */
.vista-principal, .vista-principal * {
  color: #000000 !important;
}

.cover-wrap {
  background: #f3f4f6;
  padding: 32px 16px;
  border-radius: 12px;
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

st.markdown('<div class="vista-principal">', unsafe_allow_html=True)

st.markdown(
    f"""
<div class="cover-wrap">
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
</div>
""",
    unsafe_allow_html=True,
)

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
