# Proyecto: Búsqueda y validación de patrones en textos y sistemas interactivos

## Objetivo general

Desarrollar una aplicación o solución que permita detectar y validar patrones dentro de textos mediante expresiones regulares y autómatas, así como verificar la entrada de datos en interfaces interactivas, asegurando que cumplan con criterios sintácticos y estructurales previamente definidos.

---

## Resultados de aprendizaje

- **R.A.1:** Utilizar los componentes, procedimientos y características de los análisis léxicos y sintácticos, aplicándolos de manera práctica en ejercicios que forman parte del proceso de creación de software o en el análisis de un lenguaje de programación.

- **R.A.2:** Identificar los componentes clave de la teoría de lenguajes formales con el propósito de analizar situaciones que posibiliten su diseño, empleando métodos y técnicas para desarrollar habilidades que permitan integrar estos conocimientos en el ámbito disciplinario.

- **R.A.3:** Aplicar elementos conceptuales de aprendizaje automático como parte del quehacer profesional, favoreciendo la interacción humano-computador, la toma de decisiones y el pensamiento crítico, con el fin de responder a necesidades reales mediante soluciones basadas en teoría de lenguajes formales.

---

## Descripción del proyecto

El proyecto consiste en desarrollar una aplicación orientada al reconocimiento y validación de patrones en:

- Textos  
- Documentos  
- Cadenas de caracteres  
- Archivos  

Además, permitirá verificar datos ingresados por usuarios en interfaces interactivas.

Se emplearán:

- Expresiones regulares  
- Criterios sintácticos  
- Fundamentos de autómatas  

La solución deberá:

- Aceptar  
- Rechazar  
- Extraer información  

según reglas previamente definidas.

---

## Planteamiento del proyecto

### A. Búsqueda y validación de patrones en textos

El objetivo es identificar y extraer información específica en textos usando expresiones regulares.

La aplicación deberá:

- Reconocer patrones definidos  
- Reportar coincidencias claramente  
- Validar la estructura de la información encontrada  

#### Ejemplos de patrones

- Correos electrónicos  
- Números telefónicos  
- Fechas  
- Identificadores o documentos  
- URLs  
- Placas de vehículos  
- Otros según el contexto  

---

### B. Validación de entradas en sistemas interactivos

Se enfoca en formularios donde el usuario ingresa datos.

Cada campo debe:

- Validarse en tiempo real o antes del envío  
- Cumplir formato esperado  
- Mostrar errores claros si hay inconsistencias  

#### Ejemplos de validaciones

- Formato de correo electrónico  
- Contraseña segura  
- Teléfonos (longitud y estructura)  
- Fechas válidas  
- Restricciones en usuarios o códigos  

---

## Fases del proyecto

1. **Análisis de requerimientos**
   - Identificar patrones a validar o extraer  
   - Definir contexto de la aplicación  
   - Definir tipo de interfaz  

2. **Diseño**
   - Definir entorno en Python  
   - Crear expresiones regulares  
   - Diseñar reglas de validación  
   - Definir flujo de interacción  

3. **Implementación**
   - Funciones para detectar patrones  
   - Formularios con validación automática  
   - Integración en interfaz funcional  

4. **Pruebas y casos de uso**
   - Evaluar con datos válidos e inválidos  
   - Verificar comportamiento esperado  
   - Validar manejo de errores  

5. **Documentación**
   - Explicar expresiones regulares  
   - Describir funcionamiento  
   - Mostrar ejemplos de prueba  
   - Crear guía de usuario  

---

## Entregables

- Documento del proyecto:
  - Portada  
  - Objetivo general  
  - Descripción  
  - Desarrollo  
  - Conclusiones  

- Código fuente organizado  
- Evidencias de funcionamiento (patrones en texto)  
- Evidencias de interfaz interactiva  
- Tabla de casos de prueba (éxitos y fallos)  
- Sustentación o presentación  

---

## Tecnologías y herramientas recomendadas

- **Lenguaje:** Python  
- **Librerías principales:** tkinter (o similares)  
- **Librerías opcionales:** pandas  

> ⚠️ Importante:  
> Las expresiones regulares deben implementarse manualmente (sin usar librerías predefinidas de Python para regex).

---

## Rúbrica

| Criterio | Peso |
|--------|------|
| Análisis de requerimientos y diseño | 15% |
| Implementación de búsqueda de patrones (sin regex predefinido) | 20% |
| Validación en sistemas interactivos | 20% |
| Pruebas y casos de uso | 15% |
| Documentación técnica y guía de usuario | 15% |
| Organización del código | 10% |
| Sustentación | 5% |

