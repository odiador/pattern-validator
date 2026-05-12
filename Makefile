.PHONY: help run test install clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install  - Instala las dependencias del proyecto"
	@echo "  make run      - Ejecuta la aplicación Streamlit"
	@echo "  make test     - Ejecuta las pruebas unitarias con pytest"
	@echo "  make clean    - Elimina archivos temporales de Python"

run:
	streamlit run app.py

test:
	python3 -m pytest tests/test_automata.py

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
