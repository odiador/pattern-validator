import pandas as pd
import streamlit as st

from core.automata_core import (
    validar_correo,
    validar_fecha,
    validar_telefono,
    validar_url,
    validar_placa,
    validar_password,
)

st.set_page_config(page_title="Validacion de formularios", layout="wide")

st.title("Modulo B: Validacion de formularios")

st.markdown(
    """
Ingrese los datos y valide su estructura mediante automatas finitos. Este modulo
no utiliza expresiones regulares y entrega resultados detallados para cada campo.
"""
)

if "historial" not in st.session_state:
    st.session_state["historial"] = []

with st.form("formulario_validacion"):
    st.subheader("Datos de entrada")
    correo = st.text_input("Correo electronico")
    telefono = st.text_input("Telefono")
    fecha = st.text_input("Fecha (DD/MM/AAAA o DD-MM-AAAA)")
    url = st.text_input("URL (http o https)")
    placa = st.text_input("Placa de vehiculo")
    password = st.text_input("Contrasena", type="password")
    enviar = st.form_submit_button("Validar")

if enviar:
    def evaluar(campo: str, valor: str, validador) -> dict:
        if not valor:
            return {
                "campo": campo,
                "valor": "",
                "valido": False,
                "detalle": "vacio",
            }
        valido = validador(valor)
        return {
            "campo": campo,
            "valor": valor,
            "valido": bool(valido),
            "detalle": "valido" if valido else "invalido",
        }

    resultados = [
        evaluar("correo", correo, validar_correo),
        evaluar("telefono", telefono, validar_telefono),
        evaluar("fecha", fecha, validar_fecha),
        evaluar("url", url, validar_url),
        evaluar("placa", placa, validar_placa),
        evaluar("contrasena", password, validar_password),
    ]

    df = pd.DataFrame(resultados)
    st.subheader("Resultado de validacion")
    st.dataframe(df, use_container_width=True)

    resumen = df["valido"].value_counts().reset_index()
    resumen.columns = ["estado", "total"]
    st.dataframe(resumen, use_container_width=True)

    st.session_state["historial"].append(
        {
            "intentos": len(df),
            "validos": int(df["valido"].sum()),
            "invalidos": int((~df["valido"]).sum()),
        }
    )

if st.session_state["historial"]:
    with st.expander("Historial de validaciones"):
        st.dataframe(pd.DataFrame(st.session_state["historial"]), use_container_width=True)