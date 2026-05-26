# Documentacion de Arquitectura e Implementacion

## 1. Vision General del Sistema

El sistema es una aplicacion web modular desarrollada en Python diseñada para la identificacion, extraccion y validacion de patrones de texto. La restriccion principal del proyecto exige la omision de bibliotecas de expresiones regulares (como el modulo `re` predeterminado en Python). En su lugar, el nucleo de procesamiento opera mediante la implementacion directa de Maquinas de Estados Finitos (FSM) y analizadores lexicos secuenciales.

La interfaz de usuario se implementa utilizando el framework Streamlit, permitiendo interaccion en tiempo real tanto para el analisis de bloques de texto (extraccion) como para la validacion de formularios (verificacion de entradas). El diseño prioriza la usabilidad y la exposicion clara de los resultados algoritmicos.

## 2. Arquitectura del Sistema

El patron arquitectonico sigue un modelo basado en capas con acoplamiento debil, diseñado especificamente para aprovechar el ciclo de ejecucion reactivo de Streamlit y el procesamiento de datos estructurados con Pandas. El sistema se estructura en las siguientes tres capas fundamentales:

*   **Capa de Presentacion y Estado (Frontend interactivo):** 
    Gestionada integralmente por Streamlit. Administra el ciclo de vida de la aplicacion, el estado de sesion (`st.session_state`), el enrutamiento multipagina y la captura de eventos. Delega la validacion logica a las capas inferiores y se apoya nativamente en el ecosistema de Pandas para la renderizacion eficiente de metricas y tablas de resultados visuales.
*   **Capa de Preprocesamiento y Estructuracion de Datos (Middleware):** 
    Opera como puente de integracion. Recibe los flujos de texto crudos desde la interfaz, formatea las secuencias y construye tokens evaluables. Una vez validados por el nucleo matematico, empaqueta los resultados de aceptacion en estructuras de datos tabulares (DataFrames de Pandas) para su inyeccion directa en los componentes de GUI.
*   **Capa de Logica Formal (Motor de Automatas):** 
    Constituye el nucleo matematico del proyecto. Contiene la definicion aislada de los Automatas Finitos Deterministas (DFA) modelados mediante funciones puras de Python. Recibe estructuras lexicas unitarias, las procesa mediante recorrido secuencial (caracter por caracter) y emite veredictos de aceptacion o rechazo. Este diseño determinista y exento de estado global garantiza latencia minima y compatibilidad absoluta con el modelo de ejecucion y recarga automatica de Streamlit, prescindiendo por completo de bibliotecas de expresiones regulares.

## 3. Plan de Implementacion Paso a Paso

El desarrollo se estructurara en cinco fases iterativas, alineadas rigurosamente con los requerimientos del proyecto.

### Fase 1: Analisis de Requerimientos y Diseño Teorico
1.  **Definicion de Lenguajes Formales:** Modelado matematico de las gramaticas regulares y diseño de los grafos de transicion de estados (DFA) para cada patron:
    *   Correos electronicos.
    *   Numeros telefonicos (formatos nacionales e internacionales).
    *   Fechas (formatos estandarizados como DD/MM/AAAA).
    *   URLs de recursos web.
    *   Placas de vehiculos.
    *   Validacion de contraseñas seguras (longitud, combinacion de caracteres).
2.  **Especificacion de Casos de Prueba:** Definicion de matrices de verdad con cadenas de aceptacion y rechazo teoricas para validar la correctitud del modelo antes de programar.

## 3. Plan de Implementacion Paso a Paso

El desarrollo se estructurara en cinco fases iterativas, alineadas rigurosamente con los requerimientos del proyecto y el desacoplamiento de componentes.

### Fase 1: Analisis de Requerimientos y Diseño Teorico
1.  **Definicion de Lenguajes Formales:** Modelado matematico de las gramaticas regulares y diseño de los grafos de transicion de estados (DFA) para cada patron:
    *   Correos electronicos.
    *   Numeros telefonicos (formatos nacionales e internacionales).
    *   Fechas (formatos estandarizados como DD/MM/AAAA).
    *   URLs de recursos web.
    *   Placas de vehiculos.
    *   Validacion de contraseñas seguras (longitud, combinacion de caracteres).
2.  **Especificacion de Casos de Prueba:** Definicion de matrices de verdad con cadenas de aceptacion y rechazo teoricas para validar la correctitud del modelo antes de programar.

### Fase 2: Construccion del Motor Algoritmico y Middleware de Datos
1.  **Desarrollo de la Capa de Logica Formal:** Implementacion de las transiciones de estado puras para cada DFA diseñado, asegurando el aislamiento funcional.
2.  **Aislamiento y Verificacion Sintactica:** Garantizar la ausencia total de la biblioteca `re` en todos los modulos de procesamiento.
3.  **Implementacion del Middleware de Estructuracion:** Desarrollo de funciones de puente que transformen los veredictos de los automatas en objetos de datos estructurados.
4.  **Integracion con Pandas:** Creacion de logica para envolver las colecciones de resultados (tokens aceptados/rechazados) en estructuras tabulares de alto nivel, facilitando su consumo por los componentes de interfaz.

### Fase 3: Integracion de Interfaz Grafica Reactiva (Capa de Presentacion)
Construccion de la experiencia de usuario aprovechando la naturaleza reactiva del framework y la capacidad de visualizacion de datos.

1.  **Módulo de Analisis de Textos Estructurado:**
    *   Interfaz para el procesamiento de flujos de texto con visualizacion de resultados mediante componentes de datos y columnas comparativas.
    *   Exposicion de metricas de rendimiento y conteos de patrones mediante la agregacion de datos tabulares.
2.  **Módulo de Validacion de Sistemas Interactivos:**
    *   Formularios reactivos con gestion de estado persistente durante la entrada de datos del usuario.
    *   Retroalimentacion inmediata basada en los veredictos del motor de automatas sin recargas de pagina innecesarias.
    *   Renderizado de registros de auditoria sobre los intentos de ingreso realizados.

### Fase 4: Pruebas de Integracion y Validacion de Casos de Uso
1.  **Inyeccion Exhaustiva de Datos:** Sometimiento de los formularios y del analizador de textos a casos de fallos estructurados.
2.  **Auditoria de Rendimiento en FSM:** Evaluacion del tiempo de respuesta del motor manual versus volumenes de datos mayores.
3.  **Revision de Confinamiento de Errores:** Comprobacion de que ingresos invalidos no generan excepciones criticas del sistema, sino que son manejados elegantemente por la interfaz.

### Fase 5: Compilacion Documental y Cierre
1.  Redaccion del manual tecnico, incluyendo diagramas logicos de los automatas desarrollados.
2.  Elaboracion del manual de usuario final.
3.  Documentacion de los fundamentos del aprendizaje automatico y el analisis lexico abordados en el proyecto (satisfaciendo los resultados de aprendizaje R.A.1, R.A.2 y R.A.3).

## 4. Requisitos del Entorno

Para levantar el entorno de desarrollo, el sistema requiere una version de Python 3.8 o superior.

### Dependencias
La unica dependencia externa del sistema es el entorno de visualizacion y manejo de datos estructurados.

```text
streamlit>=1.30.0
pandas>=2.0.0
```

### Instrucciones de Ejecucion

1. Configurar un entorno virtual aislado utilizando Conda:
`conda create --name pattern_env python=3.10`

2. Activar el entorno virtual:
`conda activate pattern_env`

3. Instalar dependencias requeridas:
`pip install streamlit pandas`

4. Ejecutar el servidor de desarrollo:
`streamlit run app.py`

5. Pruebas a nivel subyacente (sin interfaz de usuario):
`python core/automata_core.py`
