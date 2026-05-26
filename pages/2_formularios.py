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

Este modulo no utiliza expresiones regulares. La validacion se actualiza automaticamente mientras escribe.
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

REGLAS = {
    "correo": [
        "Estructura: usuario@dominio.tld",
        "Usuario: letras/numeros y caracteres permitidos: . _ -",
        "Dominio: letras/numeros y guiones",
        "TLD (extension): 2 a 24 letras",
    ],
    "telefono": [
        "Debe contener entre 7 y 15 digitos (los separadores se permiten)",
        "Se permiten: +, (), espacios, guiones y puntos",
        "No se permiten letras",
    ],
    "fecha": [
        "Formato: DD/MM/AAAA o DD-MM-AAAA",
        "Dia y mes en rango valido, y fecha coherente con calendario (bisiesto incluido)",
    ],
    "url": [
        "Debe iniciar con http:// o https://",
        "Dominio valido (soporta localhost) y TLD alfabetico (2-24)",
        "Opcional: puerto (ej: :8080) y ruta",
    ],
    "placa": [
        "Formato: LLL-000 o LLL000",
        "3 letras seguidas de 3 digitos",
    ],
    "contrasena": [
        "Longitud: 8 a 32 caracteres",
        "Al menos: 1 mayuscula, 1 minuscula, 1 numero y 1 caracter especial",
        "No permite espacios",
    ],
}

if "historial" not in st.session_state:
    st.session_state["historial"] = []

# En Streamlit, el evento de cambio del input puede depender del foco/tecla Enter.
# Para que el feedback se vea en cuanto el valor cambia, detectamos cambios comparando el valor actual vs. el anterior.
if "_prev_values" not in st.session_state:
    st.session_state["_prev_values"] = {}
if "touched" not in st.session_state:
    st.session_state["touched"] = {key: False for key, _, _, _ in CAMPOS}

for key, _, _, _ in CAMPOS:
    actual = st.session_state.get(key, "")
    anterior = st.session_state["_prev_values"].get(key, "")
    if actual != anterior:
        st.session_state["touched"][key] = True
        st.session_state["_prev_values"][key] = actual


def _faltantes_password(valor: str) -> list[str]:
    faltantes: list[str] = []
    if not (8 <= len(valor) <= 32):
        faltantes.append("longitud 8-32")
    if " " in valor:
        faltantes.append("sin espacios")
    if not any(c.islower() for c in valor):
        faltantes.append("al menos 1 minuscula")
    if not any(c.isupper() for c in valor):
        faltantes.append("al menos 1 mayuscula")
    if not any(c.isdigit() for c in valor):
        faltantes.append("al menos 1 numero")
    if not any((not c.isalnum()) for c in valor):
        faltantes.append("al menos 1 caracter especial")
    return faltantes


def _hints(campo_key: str, valor: str) -> list[str]:
    valor = valor or ""
    hints: list[str] = []

    if campo_key == "contrasena":
        return _faltantes_password(valor)

    if campo_key == "telefono":
        digitos = sum(1 for c in valor if c.isdigit())
        if digitos < 7 or digitos > 15:
            hints.append(f"cantidad de digitos entre 7 y 15 (actual: {digitos})")
        if any(c.isalpha() for c in valor):
            hints.append("no usar letras")
        return hints

    if campo_key == "correo":
        if "@" not in valor:
            hints.append("debe contener '@'")
            return hints
        usuario, _, dominio = valor.partition("@")
        if not usuario:
            hints.append("usuario no puede estar vacio")
        if "." not in dominio:
            hints.append("dominio debe contener punto (ej: ejemplo.com)")
        else:
            _, _, tld = dominio.rpartition(".")
            if len(tld) < 2:
                hints.append("TLD debe tener al menos 2 letras")
        return hints

    if campo_key == "url":
        if not (valor.startswith("http://") or valor.startswith("https://")):
            hints.append("debe iniciar con http:// o https://")
        return hints

    if campo_key == "placa":
        v = valor.strip().upper()
        if len(v) >= 3 and not all(c.isalpha() for c in v[:3]):
            hints.append("las primeras 3 posiciones deben ser letras")
        dig = "".join(c for c in v if c.isdigit())
        if len(dig) != 3:
            hints.append("debe contener exactamente 3 digitos")
        return hints

    if campo_key == "fecha":
        if "/" not in valor and "-" not in valor:
            hints.append("use separador '/' o '-'")
            return hints
        sep = "/" if "/" in valor else "-"
        partes = valor.split(sep)
        if len(partes) != 3:
            hints.append("use formato DD/MM/AAAA o DD-MM-AAAA")
            return hints
        d, m, a = partes
        if not (d.isdigit() and m.isdigit() and a.isdigit()):
            hints.append("use solo numeros en dia/mes/anio")
        if len(a) != 4:
            hints.append("anio debe tener 4 digitos")
        return hints

    return hints


def evaluar(campo_key: str, valor: str, validador, touched: bool) -> dict:
    valor = valor or ""

    valor_mostrar = "*" * len(valor) if campo_key == "contrasena" and valor else valor

    if not valor:
        if touched:
            return {"campo": campo_key, "valor": valor_mostrar, "valido": False, "detalle": "requerido"}
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

    st.caption("Requisitos:")
    st.markdown("\n".join([f"- {r}" for r in REGLAS.get(campo_key, [])]))

    if not touched and not valor:
        st.caption("Estado: pendiente")
        return

    if not valor:
        st.warning("Estado: requerido (campo vacio)")
        return

    if validador(valor):
        st.success("Estado: valido")
        return

    faltantes = _hints(campo_key, valor)
    st.error("Estado: invalido")
    if faltantes:
        st.caption("Que falta / que ajustar:")
        st.markdown("\n".join([f"- {f}" for f in faltantes]))


st.subheader("Datos de entrada")

col1, col2 = st.columns(2, gap="large")

with col1:
    correo = st.text_input("Correo electronico", key="correo")
    render_feedback("correo", correo, validar_correo)

    telefono = st.text_input("Telefono", key="telefono")
    render_feedback("telefono", telefono, validar_telefono)

    fecha = st.text_input("Fecha (DD/MM/AAAA o DD-MM-AAAA)", key="fecha")
    render_feedback("fecha", fecha, validar_fecha)

with col2:
    url = st.text_input("URL (http o https)", key="url")
    render_feedback("url", url, validar_url)

    placa = st.text_input("Placa de vehiculo", key="placa")
    render_feedback("placa", placa, validar_placa)

    password = st.text_input("Contrasena", type="password", key="contrasena")
    render_feedback("contrasena", password, validar_password)

resultados = [
    evaluar(key, st.session_state.get(key, ""), validador, st.session_state["touched"].get(key, False))
    for key, _, validador, _ in CAMPOS
]

df = pd.DataFrame(resultados)

st.subheader("Resumen (tiempo real)")
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
        st.session_state["_prev_values"] = {}
        st.rerun()

if st.session_state["historial"]:
    with st.expander("Historial de validaciones"):
        st.dataframe(pd.DataFrame(st.session_state["historial"]), use_container_width=True, hide_index=True)
