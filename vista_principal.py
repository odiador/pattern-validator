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
        f"URL de ejecución (local): {LOCAL_URL} (al correr `make run` / `streamlit run app.py`)"
    )

    st.markdown(
        f"""
## Documento del proyecto

### Portada

La portada se muestra al inicio de esta vista (logo UQ + datos del documento).

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


logo_b64 = _img_base64("UQ.png")
_render_cover(logo_b64)
_render_solution_spec()
