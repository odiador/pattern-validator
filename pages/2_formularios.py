import pandas as pd
import streamlit as st

from core import automata_core as fsm
from core import regex_core as regex

st.title("Modulo B: Validacion de formularios")

st.markdown(
    """
Ingrese los datos y valide su estructura mediante automatas finitos.

Este modulo no utiliza expresiones regulares. La validacion se actualiza automaticamente mientras escribe.
"""
)

motor = st.radio(
    "Motor de validacion",
    ["FSM (sin regex)", "Regex (re)"],
    horizontal=True,
)

validadores = {
    "FSM (sin regex)": {
        "correo": fsm.validar_correo,
        "telefono": fsm.validar_telefono,
        "fecha": fsm.validar_fecha,
        "url": fsm.validar_url,
        "placa": fsm.validar_placa,
        "contrasena": fsm.validar_password,
    },
    "Regex (re)": {
        "correo": regex.validar_correo,
        "telefono": regex.validar_telefono,
        "fecha": regex.validar_fecha,
        "url": regex.validar_url,
        "placa": regex.validar_placa,
        "contrasena": regex.validar_password,
    },
}[motor]

CAMPOS = [
    ("correo", "Correo electronico", validadores["correo"], {"type": None}),
    ("telefono", "Telefono", validadores["telefono"], {"type": None}),
    ("fecha", "Fecha (DD/MM/AAAA o DD-MM-AAAA)", validadores["fecha"], {"type": None}),
    ("url", "URL (http o https)", validadores["url"], {"type": None}),
    ("placa", "Placa de vehiculo", validadores["placa"], {"type": None}),
    ("contrasena", "Contrasena", validadores["contrasena"], {"type": "password"}),
]

REGLAS = {
    "correo": [
        "Estructura: usuario@dominio.tld",
        "Usuario: letras/numeros y caracteres permitidos: . _ -",
        "Dominio: letras/numeros y guiones",
        "TLD (extension): 2 a 24 letras",
    ],
    "telefono": [
        "Prefijo opcional: +57 (para Colombia)",
        "Debe iniciar con el dígito 3",
        "Debe contener exactamente 10 dígitos principales (se permiten separadores comunes)",
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
        "Formato: LLL-000, LLL000, LLL-00L o LLL00L",
        "3 letras seguidas de 2 digitos y (digito o letra) al final",
    ],
    "contrasena": [
        "Longitud: 8 a 32 caracteres",
        "Al menos: 1 mayuscula, 1 minuscula, 1 numero y 1 caracter especial",
        "No permite espacios",
        "Símbolos permitidos: ! @ # $ % ^ & * ( ) - _ = + [ ] { } ; : , . ? / \\ | ~",
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

    permitidos = set("!@#$%^&*()-_=+[]{};:,.?/\\|~")
    if not any((not c.isalnum()) for c in valor):
        faltantes.append("al menos 1 caracter especial")

    invalidos = sorted({c for c in valor if (not c.isalnum()) and (not c.isspace()) and (c not in permitidos)})
    if invalidos:
        faltantes.append("use solo símbolos permitidos (ej: ! @ # $ % ^ & * ( ) - _ = + [ ] { } ; : , . ? / \\ | ~)")

    return faltantes


def _hints(campo_key: str, valor: str) -> list[str]:
    valor = valor or ""
    hints: list[str] = []

    if campo_key == "contrasena":
        return _faltantes_password(valor)

    if campo_key == "telefono":
        import re
        digitos = "".join(re.findall(r"\d", valor))
        if any(c.isalpha() for c in valor):
            hints.append("no usar letras")
        
        if digitos.startswith("57"):
            if len(digitos) != 12:
                hints.append(f"debe tener exactamente 10 dígitos después de +57 (leídos: {len(digitos)-2})")
            if len(digitos) >= 3 and digitos[2] != "3":
                hints.append("el número debe iniciar con 3")
        else:
            if len(digitos) != 10:
                hints.append(f"debe tener exactamente 10 dígitos (actual: {len(digitos)})")
            if len(digitos) >= 1 and digitos[0] != "3":
                hints.append("el número debe iniciar con 3")
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

        if len(v) < 6:
            hints.append("use formato LLL000, LLL-000, LLL00L o LLL-00L")
            return hints

        if len(v) >= 3 and not all(c.isalpha() for c in v[:3]):
            hints.append("las primeras 3 posiciones deben ser letras")

        if len(v) == 7 and v[3] == "-":
            sufijo = v[4:7]
        elif len(v) == 6:
            sufijo = v[3:6]
        else:
            hints.append("use formato LLL000, LLL-000, LLL00L o LLL-00L")
            return hints

        if len(sufijo) != 3:
            hints.append("la parte final debe tener 3 caracteres")
            return hints

        if not (sufijo[0].isdigit() and sufijo[1].isdigit()):
            hints.append("los primeros 2 caracteres finales deben ser digitos")

        if not (sufijo[2].isdigit() or sufijo[2].isalpha()):
            hints.append("el ultimo caracter debe ser digito o letra")

        return hints

    if campo_key == "fecha":
        if "(" in valor or ")" in valor:
            hints.append("no se permiten parentesis en la fecha")
            return hints
        
        valor_limpio = valor.strip()
        
        if len(valor_limpio) != 10:
            hints.append("debe tener exactamente 10 caracteres (formato DD/MM/AAAA o DD-MM-AAAA)")
        
        if "/" not in valor_limpio and "-" not in valor_limpio:
            hints.append("use separador '/' o '-'")
            return hints
        
        sep = "/" if "/" in valor_limpio else "-"
        partes = valor_limpio.split(sep)
        if len(partes) != 3:
            hints.append("use formato DD/MM/AAAA o DD-MM-AAAA")
            return hints
        
        d, m, a = partes
        if not (d.isdigit() and m.isdigit() and a.isdigit()):
            hints.append("use solo numeros en dia/mes/anio")
            return hints
            
        if len(d) != 2:
            hints.append("dia debe tener 2 digitos")
        if len(m) != 2:
            hints.append("mes debe tener 2 digitos")
        if len(a) != 4:
            hints.append("anio debe tener 4 digitos")
            
        # Validación de rango numérico coherente con calendario
        if d.isdigit() and m.isdigit() and a.isdigit():
            d_i, m_i, a_i = int(d), int(m), int(a)
            if m_i < 1 or m_i > 12:
                hints.append("mes debe estar entre 01 y 12")
            if d_i < 1:
                hints.append("dia debe ser mayor a 0")
                
            if 1 <= m_i <= 12 and d_i >= 1:
                def es_bisiesto(valor_anio: int) -> bool:
                    return (valor_anio % 4 == 0 and valor_anio % 100 != 0) or (valor_anio % 400 == 0)
                dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if m_i == 2 and es_bisiesto(a_i):
                    dias_por_mes[1] = 29
                if d_i > dias_por_mes[m_i - 1]:
                    hints.append(f"dia invalido para el mes especificado (max {dias_por_mes[m_i - 1]} dias)")
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


EJEMPLOS_FORM = {
    "(Ninguno)": {
        "correo": "",
        "telefono": "",
        "fecha": "",
        "url": "",
        "placa": "",
        "contrasena": ""
    },
    "Ejemplos Válidos": {
        "correo": "juan.amador@example.com",
        "telefono": "+57 (312) 555-0199",
        "fecha": "29/02/2024",
        "url": "https://www.uq.edu.co",
        "placa": "ABC-123",
        "contrasena": "Secure123!"
    },
    "Ejemplos Inválidos": {
        "correo": "juan.amador@",
        "telefono": "123456789",
        "fecha": "31/04/2025",
        "url": "http://invalid-ip:99999",
        "placa": "AB-12",
        "contrasena": "short"
    },
    "Ejemplos Mezclados / Extraños": {
        "correo": "valeria.fz@uq.edu.co",
        "telefono": "320-555-0123",
        "fecha": "26-05-2026",
        "url": "http://localhost:8080/health",
        "placa": "AAA00C",
        "contrasena": "P@ssw0rd2026"
    },
    "Caso Límite 1: Años Bisiestos y Separador '-'": {
        "correo": "bisiesto.test@domain.com",
        "telefono": "3001234567",
        "fecha": "29-02-2024",
        "url": "http://localhost:3000",
        "placa": "AAA-00C",
        "contrasena": "LeapYear2024!"
    },
    "Caso Límite 2: IPs Extremas y Placas LLL000": {
        "correo": "ip.tester@sub.domain.co",
        "telefono": "+573123456789",
        "fecha": "31/12/1999",
        "url": "https://255.255.255.255:443/path",
        "placa": "XYZ987",
        "contrasena": "P@ssw0rd9999!"
    },
    "Caso Inválido 1: Teléfonos con letras / URL sin Protocolo": {
        "correo": "user@domain",
        "telefono": "312abc4567",
        "fecha": "30/02/2024",
        "url": "google.com",
        "placa": "ABC-1234",
        "contrasena": "short"
    },
    "Caso Inválido 2: Fechas del Calendario inexistentes": {
        "correo": "@domain.com",
        "telefono": "2123456789",
        "fecha": "31/11/2026",
        "url": "http://256.0.0.1",
        "placa": "123-ABC",
        "contrasena": "password_sin_especial_ni_mayuscula1"
    }
}


def _on_ejemplo_form_change():
    sel = st.session_state.get("sel_ejemplo_form", "(Ninguno)")
    valores = EJEMPLOS_FORM.get(sel, {})
    for key, val in valores.items():
        st.session_state[key] = val
        if "touched" in st.session_state:
            st.session_state["touched"][key] = bool(val)
        if "_prev_values" in st.session_state:
            st.session_state["_prev_values"][key] = val


with st.expander("Valores de ejemplo (para sustentación)", expanded=True):
    categoria_form = st.selectbox(
        "Escenarios de prueba para el formulario",
        list(EJEMPLOS_FORM.keys()),
        key="sel_ejemplo_form",
        on_change=_on_ejemplo_form_change,
    )
    if st.button("Cargar / Reiniciar escenario"):
        _on_ejemplo_form_change()


st.subheader("Datos de entrada")

# Fila 1: Correo y Teléfono
row1_col1, row1_col2 = st.columns(2, gap="large")
with row1_col1:
    with st.container(border=True):
        st.markdown("##### Correo electrónico")
        correo = st.text_input("Correo electrónico", key="correo", label_visibility="collapsed")
        render_feedback("correo", correo, validadores["correo"])
with row1_col2:
    with st.container(border=True):
        st.markdown("##### Teléfono")
        telefono = st.text_input("Teléfono", key="telefono", label_visibility="collapsed")
        render_feedback("telefono", telefono, validadores["telefono"])

# Fila 2: Fecha y URL
row2_col1, row2_col2 = st.columns(2, gap="large")
with row2_col1:
    with st.container(border=True):
        st.markdown("##### Fecha (DD/MM/AAAA o DD-MM-AAAA)")
        fecha = st.text_input("Fecha", key="fecha", label_visibility="collapsed")
        render_feedback("fecha", fecha, validadores["fecha"])
with row2_col2:
    with st.container(border=True):
        st.markdown("##### URL (http o https)")
        url = st.text_input("URL", key="url", label_visibility="collapsed")
        render_feedback("url", url, validadores["url"])

# Fila 3: Placa y Contraseña
row3_col1, row3_col2 = st.columns(2, gap="large")
with row3_col1:
    with st.container(border=True):
        st.markdown("##### Placa de vehículo")
        placa = st.text_input("Placa de vehículo", key="placa", label_visibility="collapsed")
        render_feedback("placa", placa, validadores["placa"])
with row3_col2:
    with st.container(border=True):
        st.markdown("##### Contraseña")
        password = st.text_input("Contraseña", type="password", key="contrasena", label_visibility="collapsed")
        render_feedback("contrasena", password, validadores["contrasena"])

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
