# Manual del Usuario y Documentación Técnica

## 1. Introducción
Este sistema permite la búsqueda y validación de patrones en textos y formularios sin el uso de expresiones regulares (módulo `re`), empleando en su lugar Autómatas Finitos Deterministas (DFA) implementados manualmente en Python.

## 2. Guía de Usuario

### Módulo A: Analizador de Textos
1. Acceda a la página **Analizador de Texto** desde el menú lateral.
2. Ingrese el texto manualmente en el área de texto o cargue un archivo `.txt` o `.log`.
3. Presione el botón **Analizar patrones**.
4. El sistema mostrará:
   - Una tabla con todos los patrones encontrados (Correos, Teléfonos, Fechas, URLs, Placas).
   - Métricas comparativas y un resumen por tipo de patrón.

### Módulo B: Validación de Formularios
1. Acceda a la página **Formularios** desde el menú lateral.
2. Complete los campos requeridos (Correo, Teléfono, Fecha, URL, Placa, Contraseña).
3. A medida que escribe, el sistema validará cada campo en tiempo real y mostrará si es **válido**, **inválido** o **pendiente**.
4. Si desea registrar un intento, presione **Guardar intento en historial**. El sistema mantendrá un historial de intentos en la sesión actual.

## 3. Documentación Técnica

### Estructura de Autómatas (DFAs)

#### Validador de Correo (`validar_correo`)
- **q0:** Estado inicial, espera un carácter alfanumérico.
- **q1:** Cuerpo del usuario (antes del @). Acepta alfanuméricos, puntos, guiones y guiones bajos.
- **q2:** Después del @. Espera inicio del dominio.
- **q3:** Cuerpo del dominio. Acepta alfanuméricos y guiones.
- **q4:** Después del punto en el dominio. Espera el TLD (extensión).
- **q5:** Estado de aceptación. El TLD debe tener al menos 2 caracteres alfabéticos.

#### Validador de Teléfono (`validar_telefono`)
- Soporta formatos internacionales (`+57 ...`), paréntesis para códigos de área `(601) ...`, y separadores comunes como espacios, guiones y puntos.
- Valida una longitud de entre 7 y 15 dígitos numéricos totales.

#### Validador de Fecha (`validar_fecha`)
- Formatos aceptados: `DD/MM/AAAA` y `DD-MM-AAAA`.
- Incluye validación lógica de calendario (días por mes y años bisiestos).

#### Validador de URL (`validar_url`)
- Requiere prefijo `http://` o `https://`.
- Valida estructura de dominio, TLD alfabético (2-24 caracteres) y soporta puertos (e.g., `:8080`) y `localhost`.

#### Validador de Contraseña (`validar_password`)
- Longitud: 8 a 32 caracteres.
- Requisitos: Al menos una mayúscula, una minúscula, un número y un carácter especial. No permite espacios.

### Pipeline de Procesamiento
1. **Tokenización:** El texto se divide en candidatos utilizando un conjunto de caracteres permitidos para evitar rupturas innecesarias en patrones complejos (como URLs).
2. **Limpieza:** Se eliminan signos de puntuación periféricos (puntos finales, comas, paréntesis de cierre) antes de la validación.
3. **Validación:** Cada token limpio se somete a la batería de autómatas definidos en `core/automata_core.py`.
