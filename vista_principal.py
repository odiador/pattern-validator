import base64
from pathlib import Path

import streamlit as st

REPO_URL = "https://github.com/odiador/pattern-validator/tree/main/"
BLOB_URL = "https://github.com/odiador/pattern-validator/blob/main/"
LOCAL_URL = "http://localhost:8501"  # Streamlit por defecto


def _img_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _render_cover(logo_base64: str) -> None:
    template_path = Path(__file__).with_name("vista_principal_template.html")
    template = template_path.read_text(encoding="utf-8")
    cover_html = template.replace("{{LOGO_BASE64}}", logo_base64)
    st.html(cover_html)


def _render_solution_spec() -> None:
    st.title("Solución implementada (especificación técnica)")

    st.info(
        f"Repositorio (remoto): {REPO_URL}\n\n"
    )

    st.markdown(
        f"""
### Objetivo general

Implementar una aplicación web que permita **extraer** y **validar** patrones frecuentes (correos, teléfonos, fechas, URLs, placas y contraseñas) en dos contextos:

- **Texto libre / archivos** (extracción de coincidencias válidas).
- **Interfaces interactivas** (validación de entradas con feedback claro).

### Descripción

- **Tecnología:** Streamlit (UI), Python (lógica), pandas (tablas/resúmenes).
- **Arquitectura (archivos en GitHub):**
  - [`app.py`]({BLOB_URL}app.py): enrutador con `st.navigation`.
  - [`vista_principal.py`]({BLOB_URL}vista_principal.py): documentación y guía de la solución.
  - [`pages/1_analizador_texto.py`]({BLOB_URL}pages/1_analizador_texto.py): Módulo A (extracción en texto).
  - [`pages/2_formularios.py`]({BLOB_URL}pages/2_formularios.py): Módulo B (validación en formularios).
  - [`core/automata_core.py`]({BLOB_URL}core/automata_core.py): validadores FSM (sin regex).
  - [`core/text_pipeline.py`]({BLOB_URL}core/text_pipeline.py): pipeline de tokenización + validación para extracción.
  - [`core/regex_core.py`]({BLOB_URL}core/regex_core.py): motor alternativo opcional basado en regex.

### Desarrollo

#### Vista 1: Vista principal ([`vista_principal.py`]({BLOB_URL}vista_principal.py))

- Muestra la **portada** y esta **especificación**.
- Incluye enlaces y comandos para ejecutar, probar y ubicar el código.

#### Vista 2: Módulo A — Análisis de textos ([`pages/1_analizador_texto.py`]({BLOB_URL}pages/1_analizador_texto.py))

**Flujo de usuario**
1. El usuario pega texto en `st.text_area` o carga `.txt/.log`.
2. Selecciona motor: **FSM (sin regex)** o **Regex (re)**.
3. Presiona **Analizar patrones**.

**Qué pasa por dentro (FSM)**
- [`core/text_pipeline.py`]({BLOB_URL}core/text_pipeline.py):
  - Tokeniza candidatos con `_tokenizar_candidatos` (solo caracteres permitidos).
  - Limpia tokens con `_limpiar_token`.
  - Prueba validadores en orden (más específicos → más generales) para evitar ambigüedades.

**Salida**
- Tabla con pares `{{tipo, valor}}` y un resumen por tipo.

#### Vista 3: Módulo B — Validación de formularios ([`pages/2_formularios.py`]({BLOB_URL}pages/2_formularios.py))

**Objetivo:** validación reactiva con feedback por campo.

**Cómo se implementó la “validación en tiempo real”**
- No se usa `st.form` (porque agrupa y valida al enviar).
- Se usan `st.text_input` y estados en `st.session_state`:
  - `touched`: marca campos que el usuario ya modificó.
  - `_prev_values`: detecta cambios comparando valor actual vs anterior.

**Feedback “exacto” por campo**
- `render_feedback(...)` muestra:
  - Reglas del campo (`REGLAS`).
  - Estado: pendiente / requerido / válido / inválido.
  - “Qué falta / qué ajustar” usando `_hints(...)` (por ejemplo, en contraseña: longitud, mayúscula, número, etc.).

**Resumen en vivo**
- Se construye un DataFrame con `evaluar(...)` y se muestra como tabla:
  - válido / inválido / pendiente.

### Conclusiones

- Se logró una solución modular (UI por páginas + núcleo en `core/`).
- La validación entrega mensajes claros por campo, evitando “solo válido/inválido”.
- En Streamlit, el “tiempo real” puede depender del foco del input (Tab/clic fuera), por eso se documenta esta limitación.
"""
    )

    st.markdown(
       f"""
## Código fuente organizado

Estructura principal:

- [`app.py`]({BLOB_URL}app.py) (router)
- [`vista_principal.py`]({BLOB_URL}vista_principal.py) (documentación)
- [`pages/`]({REPO_URL}pages) (vistas)
- [`core/`]({REPO_URL}core) (lógica de validación y extracción)
- [`tests/`]({REPO_URL}tests) (pruebas unitarias)

"""
    )

    st.markdown("## Evidencias de funcionamiento (patrones en texto)")
    st.markdown(
        """
Para evidenciar el Módulo A:
- Ingrese un texto con patrones (correo/teléfono/fecha/url/placa).
- Ejecute “Analizar patrones”.
- Tome captura de (1) tabla de resultados y (2) resumen por tipo.
"""
    )

    st.markdown("## Evidencias de interfaz interactiva")
    st.markdown(
        """
Para evidenciar el Módulo B:
- Ingrese valores inválidos y observe el feedback “qué falta/qué ajustar”.
- Corrija el valor y observe el cambio a “válido”.
- Tome capturas por campo y del resumen en vivo.
"""
    )

    st.markdown("## Tabla de casos de prueba (éxitos y fallos)")
    st.markdown(
       f"""
- Pruebas unitarias: [`tests/test_automata.py`]({BLOB_URL}tests/test_automata.py).
- Comando:
"""
    )
    st.code("make test\n# o\npytest -q", language="bash")

    st.markdown("## Sustentación o presentación")
    st.markdown(
        """
Sugerencia de demo (5–8 min):
1. Mostrar portada + objetivos.
2. Demostrar Módulo A con un texto y explicar el pipeline.
3. Demostrar Módulo B con 2–3 campos (inválido → válido) y explicar `touched/_prev_values`.
4. Mostrar ejecución de tests.
"""
    )

    st.markdown("## Autómatas (visuales)")
    st.caption("Seleccione la pestaña correspondiente para visualizar el diagrama de transiciones (FSM) de cada patrón.")

    tab_placa, tab_correo, tab_telefono, tab_fecha, tab_url, tab_pass = st.tabs([
        "Placa",
        "Correo electrónico",
        "Teléfono",
        "Fecha",
        "URL",
        "Contraseña"
    ])

    with tab_placa:
        st.markdown("### Autómata de Placas")
        st.caption("Acepta formatos LLL-000, LLL000, LLL-00L, LLL00L. L = Letra, D = Dígito.")
        dot_placa = """digraph PlacaFSM {
 rankdir=LR;
 node [shape=circle, fontsize=12];

 q0 [label="q0 (Inicio)"];
 q1 [label="q1 (L1)"];
 q2 [label="q2 (L2)"];
 q3 [label="q3 (L3)"];
 q4 [label="q4 (op -)"];
 q5 [label="q5 (D1)"];
 q6 [label="q6 (D2)"];
 q7 [shape=doublecircle, label="q7 (Acepta)"];

 q0 -> q1 [label="L"];
 q1 -> q2 [label="L"];
 q2 -> q3 [label="L"];

 q3 -> q4 [label="-"];
 q3 -> q5 [label="D"];
 q4 -> q5 [label="D"];

 q5 -> q6 [label="D"];
 q6 -> q7 [label="D | L"];
}
"""
        st.graphviz_chart(dot_placa)

    with tab_correo:
        st.markdown("### Autómata de Correo Electrónico")
        st.caption("Valida un formato estándar usuario@dominio.extension con soporte de subdominios y extensión de 2 a 24 caracteres.")
        dot_correo = """digraph CorreoFSM {
 rankdir=LR;
 node [shape=circle, fontsize=12];

 q0 [label="q0 (Inicio)"];
 q1 [label="q1 (Usuario)"];
 q2 [label="q2 (@)"];
 q3 [label="q3 (Dominio)"];
 q4 [label="q4 (.)"];
 q5 [shape=doublecircle, label="q5 (Acepta)"];

 q0 -> q1 [label="alnum"];
 q1 -> q1 [label="alnum | . | _ | -"];
 q1 -> q2 [label="@"];

 q2 -> q3 [label="alnum"];
 q3 -> q3 [label="alnum | -"];
 q3 -> q4 [label="."];

 q4 -> q5 [label="letra"];
 q5 -> q5 [label="letra"];
 q5 -> q4 [label="."];
}
"""
        st.graphviz_chart(dot_correo)

    with tab_telefono:
        st.markdown("### Autómata de Teléfono (Colombia)")
        st.caption("Valida números de teléfono en Colombia: opcional prefijo +57, número de exactamente 10 dígitos iniciando obligatoriamente con 3.")
        dot_telefono = """digraph TelefonoColFSM {
 rankdir=LR;
 node [shape=circle, fontsize=12];

 q0 [label="q0 (Inicio)"];
 qp1 [label="qp1 (+)"];
 qp2 [label="qp2 (5)"];
 qp3 [label="qp3 (7)"];
 qd1 [label="qd1 (3)"];
 qd2 [label="qd2"];
 qd3 [label="qd3"];
 qd4 [label="qd4"];
 qd5 [label="qd5"];
 qd6 [label="qd6"];
 qd7 [label="qd7"];
 qd8 [label="qd8"];
 qd9 [label="qd9"];
 qd10 [shape=doublecircle, label="qd10 (Acepta)"];

 q0 -> qp1 [label="+"];
 qp1 -> qp2 [label="5"];
 qp2 -> qp3 [label="7"];
 qp3 -> qd1 [label="3"];
 q0 -> qd1 [label="3"];

 qd1 -> qd2 [label="D"];
 qd2 -> qd3 [label="D"];
 qd3 -> qd4 [label="D"];
 qd4 -> qd5 [label="D"];
 qd5 -> qd6 [label="D"];
 qd6 -> qd7 [label="D"];
 qd7 -> qd8 [label="D"];
 qd8 -> qd9 [label="D"];
 qd9 -> qd10 [label="D"];
}
"""
        st.graphviz_chart(dot_telefono)

    with tab_fecha:
        st.markdown("### Autómata de Fecha")
        st.caption("Acepta fechas en formato DD/MM/AAAA o DD-MM-AAAA, admitiendo paréntesis balanceados. Las transiciones de paréntesis '(' y ')' se representan como bucles sobre los estados correspondientes, y adicionalmente el motor valida la cantidad de días del mes e inclusive años bisiestos.")
        dot_fecha = """digraph FechaFSM {
 rankdir=LR;
 node [shape=circle, fontsize=12];

 q0 [label="q0 (Inicio)"];
 q1 [label="q1 (D1)"];
 q2 [label="q2 (D2)"];
 q3 [label="q3 (Sep1)"];
 q4 [label="q4 (M1)"];
 q5 [label="q5 (M2)"];
 q6 [label="q6 (Sep2)"];
 q7 [label="q7 (A1)"];
 q8 [label="q8 (A2)"];
 q9 [label="q9 (A3)"];
 q10 [shape=doublecircle, label="q10 (Acepta)"];

 q0 -> q1 [label="D"];
 q1 -> q2 [label="D"];
 q2 -> q3 [label="/ | -"];
 q3 -> q4 [label="D"];
 q4 -> q5 [label="D"];
 q5 -> q6 [label="/ | - (coherente)"];
 q6 -> q7 [label="D"];
 q7 -> q8 [label="D"];
 q8 -> q9 [label="D"];
 q9 -> q10 [label="D"];

 // Autoreferencias para paréntesis balanceados
 q0 -> q0 [label="("];
 q1 -> q1 [label="( | )"];
 q2 -> q2 [label="( | )"];
 q3 -> q3 [label="( | )"];
 q4 -> q4 [label="( | )"];
 q5 -> q5 [label="( | )"];
 q6 -> q6 [label="( | )"];
 q7 -> q7 [label="( | )"];
 q8 -> q8 [label="( | )"];
 q9 -> q9 [label="( | )"];
 q10 -> q10 [label=")"];
}
"""
        st.graphviz_chart(dot_fecha)

    with tab_url:
        st.markdown("### Autómata de URL")
        st.caption("Valida URLs con protocolo http:// o https://, soportando localhost, direcciones IP válidas (octetos <= 255) o dominios con TLD alfabético (2-24).")
        dot_url = """digraph UrlFSM {
 rankdir=LR;
 node [shape=circle, fontsize=12];

 q0 [label="q0 (Inicio)"];
 q1 [label="q1 (http:// | https://)"];
 q2 [label="q2 (localhost / IP)"];
 q3 [label="q3 (Etiqueta)"];
 q4 [label="q4 (.)"];
 q5 [shape=doublecircle, label="q5 (Acepta TLD / IP)"];

 q0 -> q1 [label="http:// | https://"];
 q1 -> q2 [label="localhost | octeto_IP"];
 q1 -> q3 [label="alnum"];

 q3 -> q3 [label="alnum | -"];
 q3 -> q4 [label="."];

 q4 -> q5 [label="letra (2-24) | octeto_IP"];
 q5 -> q5 [label="letra"];
 q5 -> q4 [label="."];
}
"""
        st.graphviz_chart(dot_url)

    with tab_pass:
        st.markdown("### Autómata de Contraseña")
        st.caption("Valida la longitud mínima (8-32 caracteres), prohíbe espacios y valida la presencia de mayúsculas, minúsculas, dígitos y caracteres especiales.")
        dot_pass = """digraph PasswordFSM {
 rankdir=LR;
 node [shape=circle, fontsize=12];

 q0 [label="q0 (Inicio)"];
 q1 [label="q1 (Leído < 8 chars)"];
 q2 [shape=doublecircle, label="q2 (Acepta 8-32 chars)"];
 q_err [label="q_err (Espacio / >32)"];

 q0 -> q1 [label="[a-z]|[A-Z]|[0-9]|[símbolos]"];
 q1 -> q1 [label="[a-z]|[A-Z]|[0-9]|[símbolos]"];
 q1 -> q2 [label="[a-z]|[A-Z]|[0-9]|[símbolos] (pos >= 8)"];
 q2 -> q2 [label="[a-z]|[A-Z]|[0-9]|[símbolos] (pos < 32)"];
 q2 -> q_err [label="[\\s] (espacio) | pos > 32"];
 q1 -> q_err [label="[\\s] (espacio)"];
}
"""
        st.graphviz_chart(dot_pass)


logo_b64 = _img_base64("UQ.png")
_render_cover(logo_b64)
_render_solution_spec()
