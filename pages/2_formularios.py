import pandas as pd
import streamlit as st

from core.automata_core import (
    validar_correo,
    validar_fecha,
    validar_password,
    validar_placa,
    validar_telefono,
    validar_url,
)

st.set_page_config(page_title="Validacion de formularios", layout="wide")

st.title("Modulo B: Validacion de formularios")

st.markdown(
    """
Ingrese los datos y valide su estructura mediante automatas finitos.

Este modulo no utiliza expresiones regulares y entrega retroalimentacion en tiempo real mientras escribe.
"""
)

CAMPOS = [
    ("correo", "Correo electronico", validar_correo, {"type": None}),
    ("telefono", "Telefono", validar_telefono, {"type": None}),
    ("fecha", "Fecha (DD/MM/AAAA o DD-MM-AAAA)", validar_fecha, {"type": None}),
    ("url", "URL (http o https)", validar_url, {"type": None}),
    ("placa", "Placa de vehiculo", validar_placa, {"type": None}),
    ("contrasena", "Contrasena", validar_password, {"type": "password"}),
]

if "historial" not in st.session_state:
    st.session_state["historial"] = []

if "touched" not in st.session_state:
    st.session_state["touched"] = {key: False for key, _, _, _ in CAMPOS}


def tocar(campo_key: str) -> None:
    st.session_state["touched"][campo_key] = True


def evaluar(campo_key: str, valor: str, validador, touched: bool) -> dict:
    valor = valor or ""

    if campo_key == "contrasena":
        valor_mostrar = "*" * len(valor) if valor else ""
    else:
        valor_mostrar = valor

    if not valor:
        if touched:
            return {"campo": campo_key, "valor": valor_mostrar, "valido": False, "detalle": "vacio"}
        return {"campo": campo_key, "valor": valor_mostrar, "valido": None, "detalle": "pendiente"}

    valido = bool(validador(valor))
    return {
        "campo": campo_key,
        "valor": valor_mostrar,
        "valido": valido,
        "detalle": "valido" if valido else "invalido",
    }


def render_feedback(campo_key: str, valor: str, validador) -> None:
    touched = bool(st.session_state["touched"].get(campo_key))
    valor = valor or ""

    if not touched and not valor:
        return

    if not valor:
        st.info("Campo vacio")
        return

    if validador(valor):
        st.success("Valido")
    else:
        st.error("Invalido")


st.subheader("Datos de entrada")

col1, col2 = st.columns(2, gap="large")

with col1:
    correo = st.text_input("Correo electronico", key="correo", on_change=tocar, args=("correo",))
    render_feedback("correo", correo, validar_correo)

    telefono = st.text_input("Telefono", key="telefono", on_change=tocar, args=("telefono",))
    render_feedback("telefono", telefono, validar_telefono)

    fecha = st.text_input(
        "Fecha (DD/MM/AAAA o DD-MM-AAAA)",
        key="fecha",
        on_change=tocar,
        args=("fecha",),
    )
    render_feedback("fecha", fecha, validar_fecha)

with col2:
    url = st.text_input("URL (http o https)", key="url", on_change=tocar, args=("url",))
    render_feedback("url", url, validar_url)

    placa = st.text_input("Placa de vehiculo", key="placa", on_change=tocar, args=("placa",))
    render_feedback("placa", placa, validar_placa)

    password = st.text_input(
        "Contrasena",
        type="password",
        key="contrasena",
        on_change=tocar,
        args=("contrasena",),
    )
    render_feedback("contrasena", password, validar_password)

resultados = [
    evaluar(key, st.session_state.get(key, ""), validador, st.session_state["touched"].get(key, False))
    for key, _, validador, _ in CAMPOS
]

df = pd.DataFrame(resultados)

st.subheader("Resultado de validacion (tiempo real)")
st.dataframe(df, use_container_width=True, hide_index=True)

validos = int((df["valido"] == True).sum())
invalidos = int((df["valido"] == False).sum())
pendientes = int(df["valido"].isna().sum())

st.dataframe(
    pd.DataFrame(
        [
            {"estado": "valido", "total": validos},
            {"estado": "invalido", "total": invalidos},
            {"estado": "pendiente", "total": pendientes},
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

acciones_col1, acciones_col2 = st.columns(2)

with acciones_col1:
    if st.button("Guardar intento en historial"):
        st.session_state["historial"].append(
            {
                "intentos": int(len(df)),
                "validos": validos,
                "invalidos": invalidos,
                "pendientes": pendientes,
            }
        )

with acciones_col2:
    if st.button("Limpiar campos"):
        for key, _, _, _ in CAMPOS:
            st.session_state[key] = ""
        st.session_state["touched"] = {key: False for key, _, _, _ in CAMPOS}
        st.rerun()

if st.session_state["historial"]:
    with st.expander("Historial de validaciones"):
        st.dataframe(pd.DataFrame(st.session_state["historial"]), use_container_width=True, hide_index=True)
