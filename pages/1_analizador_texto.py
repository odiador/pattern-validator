import pandas as pd
import streamlit as st

from core.text_pipeline import analizar_texto as analizar_texto_fsm
from core.regex_core import analizar_texto as analizar_texto_regex

st.title("Modulo A: Analisis de textos")

st.markdown(
    """
Este modulo permite procesar textos largos y extraer patrones validos.

Puede usar el motor FSM (sin regex) o un motor alternativo basado en expresiones regulares.
"""
)

motor = st.radio(
    "Motor de extraccion",
    ["FSM (sin regex)", "Regex (re)"],
    horizontal=True,
)

EJEMPLOS_TEXTO = {
    "(Ninguno)": "",
    "Demo completo (todos los patrones)": (
        "En el log del 29/02/2024 se registró el usuario juan.amador@example.com y también valeria.fz@uq.edu.co. "
        "Visitaron https://www.uq.edu.co y http://localhost:8080/health. "
        "Contactos: +57 (312) 555-0199 y 320-555-0123. "
        "Placas reportadas: ABC-123, XYZ987, AAA00C y AAA-00C. "
        "Otra fecha: 26-05-2026."
    ),
    "Placas (válidas)": "Placas: ABC-123, XYZ987, AAA00C, AAA-00C.",
    "Placas (inválidas)": "Placas inválidas: AB-123, 123-ABC, AAA-0BC, ABC-12.",
    "Correos": "Correos: usuario@dominio.com, test.user_1@sub.domain.co, malo@@dominio.com.",
    "Fechas": "Fechas: 29/02/2024, 31/04/2025, 26-05-2026.",
    "URLs": "URLs: https://google.com, http://localhost:8501, ftp://site.com.",
    "Teléfonos": "Teléfonos: +57 312 555 0199, (031) 555-0123, ABC123.",
}

if "texto_usuario" not in st.session_state:
    st.session_state["texto_usuario"] = ""

def _on_ejemplo_change():
    sel = st.session_state["sel_ejemplo"]
    st.session_state["texto_usuario"] = EJEMPLOS_TEXTO.get(sel, "")

col_entrada, col_archivo = st.columns([2, 1])

with col_entrada:
    with st.expander("Textos de ejemplo (para sustentación)", expanded=True):
        categoria = st.selectbox(
            "Categoría",
            list(EJEMPLOS_TEXTO.keys()),
            key="sel_ejemplo",
            on_change=_on_ejemplo_change,
        )
        if st.button("Cargar / Recargar ejemplo"):
            st.session_state["texto_usuario"] = EJEMPLOS_TEXTO.get(categoria, "")

    texto_usuario = st.text_area(
        "Texto a analizar",
        key="texto_usuario",
        height=220,
        placeholder=(
            "Ejemplo: Puede escribir texto con correos, fechas, telefonos, URLs o placas."
        ),
    )

with col_archivo:
    archivo = st.file_uploader(
        "Cargar archivo de texto",
        type=["txt", "log"],
    )

texto_final = texto_usuario or ""
if archivo is not None:
    contenido = archivo.read().decode("utf-8", errors="ignore")
    if texto_final:
        texto_final = f"{texto_final}\n{contenido}"
    else:
        texto_final = contenido

if st.button("Analizar patrones"):
    if not texto_final.strip():
        st.error("Debe ingresar texto o cargar un archivo.")
    else:
        if motor == "Regex (re)":
            resultados = analizar_texto_regex(texto_final)
        else:
            resultados = analizar_texto_fsm(texto_final)
        st.subheader("Resultados del analisis")

        if resultados:
            df = pd.DataFrame(resultados)
            total = len(df)

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Total de patrones encontrados", value=total)
                st.dataframe(df, use_container_width=True)

            with col2:
                resumen = df["tipo"].value_counts().reset_index()
                resumen.columns = ["tipo", "total"]
                st.dataframe(resumen, use_container_width=True)
        else:
            st.warning("No se encontraron patrones validos en el contenido.")

with st.expander("Criterios de validacion"):
    st.markdown(
        """
- Correos: usuario y dominio con extensiones alfabeticas.
- Fechas: formatos DD/MM/AAAA o DD-MM-AAAA con validacion de calendario.
- Telefonos: Colombia (inicia con 3, 10 digitos exactamente, +57 opcional).
- URLs: http o https con dominio valido y TLD alfabetico.
- Placas: formato LLL-000, LLL000, LLL-00L o LLL00L.
"""
    )