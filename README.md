# Validador de Patrones con Autómatas (FSM)

Este proyecto es una aplicación web interactiva desarrollada en Python con **Streamlit** diseñada para la identificación, extracción y validación de patrones de texto (Correos, URLs, Fechas, etc.) mediante el uso de **Autómatas Finitos Deterministas (DFA)**.

⚠️ **Restricción de Implementación:** El motor de validación ha sido desarrollado desde cero **sin utilizar la librería `re` (Expresiones Regulares)** de Python, cumpliendo con los objetivos académicos de la teoría de lenguajes formales.

## 🚀 Inicio Rápido

### Requisitos previos
- Python 3.8 o superior
- Conda (opcional, recomendado)

### Instalación
1. Crear y activar el entorno (Conda):
   ```bash
   conda create --name pattern_env python=3.10 -y
   conda activate pattern_env
   ```
2. Instalar dependencias:
   ```bash
   make install
   ```

### Ejecución
Para iniciar la aplicación, simplemente ejecuta:
```bash
make run
```

## 📖 Documentación

El proyecto cuenta con documentación detallada sobre el diseño de los autómatas y el manual de usuario:

- [**Manual de Usuario y Documentación Técnica**](./MANUAL.md): Detalle de estados de los DFAs y guía de uso de la interfaz.
- [**Descripción del Proyecto**](./PROYECTO.md): Objetivos, alcances y rúbrica de evaluación.

## 🛠️ Comandos Disponibles (Makefile)

- `make`: Muestra la ayuda y lista de comandos.
- `make run`: Lanza la interfaz de Streamlit.
- `make test`: Ejecuta la suite de pruebas unitarias.
- `make clean`: Limpia archivos temporales de caché.

## 🧪 Pruebas
Las validaciones han sido probadas exhaustivamente. Puedes correr los tests con:
```bash
python3 -m pytest tests/test_automata.py
```
