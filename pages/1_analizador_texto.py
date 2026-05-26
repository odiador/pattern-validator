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

col_entrada, col_archivo = st.columns([2, 1])

with col_entrada:
    texto_usuario = st.text_area(
        "Texto a analizar",
        height=220,
        placeholder=(
            "Ejemplo: Puede escribir texto con correos, fechas, telefonos o URLs."
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
- Telefonos: 7 a 15 digitos con separadores comunes.
- URLs: http o https con dominio valido y TLD alfabetico.
- Placas: formato LLL-000, LLL000, LLL-00L o LLL00L.
"""
    )