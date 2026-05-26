import pytest
from core.automata_core import (
    validar_correo,
    validar_fecha,
    validar_telefono,
    validar_url,
    validar_placa,
    validar_password,
)

@pytest.mark.parametrize("correo, esperado", [
    ("test@example.com", True),
    ("user.name@domain.co", True),
    ("a@b.cd", True),
    ("@domain.com", False),
    ("test@", False),
    ("test@domain", False),
    ("test@.com", False),
    ("test@domain.c", False),
])
def test_validar_correo(correo, esperado):
    assert validar_correo(correo) == esperado

@pytest.mark.parametrize("fecha, esperado", [
    ("12/05/2026", True),
    ("01-01-2000", True),
    ("29/02/2024", True),
    ("(29/02/2024)", True),
    ("29/(02)/2024", True),
    ("(29-02-2024)", True),
    ("29/02/(2024)", True),
    ("32/01/2024", False),
    ("29/02/2023", False),
    ("01/01/99", False),
    ("aa/bb/cccc", False),
    ("(29/02/2024", False),
])
def test_validar_fecha(fecha, esperado):
    assert validar_fecha(fecha) == esperado

@pytest.mark.parametrize("telefono, esperado", [
    ("+57 3123456789", True),
    ("3123456789", True),
    ("+57 300 123 4567", True),
    ("300.123.4567", True),
    ("+57 (300) 123-4567", True),
    ("300-123-4567", True),
    ("(300) 123-4567", True),
    ("+57 (300).123-4567", True),
    ("123-4567", False),
    ("(601) 1234567", False),
    ("123", False),
    ("abc-defg", False),
    ("+", False),
    ("300123456", False),
    ("30012345678", False),
    ("2123456789", False),
    ("+57 (400) 123-4567", False),
    ("+58 (300) 123-4567", False),
])
def test_validar_telefono(telefono, esperado):
    assert validar_telefono(telefono) == esperado

@pytest.mark.parametrize("url, esperado", [
    ("https://google.com", True),
    ("http://localhost:8080", True),
    ("https://sub.domain.org/path?q=1", True),
    ("http://192.168.1.1", True),
    ("https://255.255.255.255:8080/path", True),
    ("http://0.0.0.0", True),
    ("http://256.0.0.1", False),
    ("http://192.168.01.1", False),
    ("http://192.168.1.2.3", False),
    ("http://192.168.1", False),
    ("https://1.2.3.4:99999/", False),
    ("google.com", False),
    ("ftp://site.com", False),
    ("http://", False),
    ("https://domain..com", False),
])
def test_validar_url(url, esperado):
    assert validar_url(url) == esperado

@pytest.mark.parametrize("placa, esperado", [
    ("ABC-123", True),
    ("XYZ987", True),
    ("AAA00C", True),
    ("AAA-00C", True),
    ("AB-123", False),
    ("ABC-12", False),
    ("AAA-0BC", False),
    ("123-ABC", False),
    ("ABCD123", False),
])
def test_validar_placa(placa, esperado):
    assert validar_placa(placa) == esperado

@pytest.mark.parametrize("password, esperado", [
    ("Secure123!", True),
    ("P@ssw0rd2026", True),
    ("short", False),
    ("nonumber", False),
    ("NOMINUS1!", False),
    ("nopunc123", False),
    ("with space 1!", False),
])
def test_validar_password(password, esperado):
    assert validar_password(password) == esperado


def test_analizar_texto_cronologico():
    from core.text_pipeline import analizar_texto as analizar_texto_fsm
    from core.regex_core import analizar_texto as analizar_texto_regex

    texto = (
        "En el log del 29/02/2024 se registró el usuario juan.amador@example.com y también valeria.fz@uq.edu.co. "
        "Visitaron https://www.uq.edu.co y http://localhost:8080/health. "
        "Contactos: +57 (312) 555-0199 y 320-555-0123. "
        "Placas reportadas: ABC-123, XYZ987, AAA00C y AAA-00C. "
        "Otra fecha: 26-05-2026."
    )
    esperado = [
        {"tipo": "fecha", "valor": "29/02/2024"},
        {"tipo": "correo", "valor": "juan.amador@example.com"},
        {"tipo": "correo", "valor": "valeria.fz@uq.edu.co"},
        {"tipo": "url", "valor": "https://www.uq.edu.co"},
        {"tipo": "url", "valor": "http://localhost:8080/health"},
        {"tipo": "telefono", "valor": "+57 (312) 555-0199"},
        {"tipo": "telefono", "valor": "320-555-0123"},
        {"tipo": "placa", "valor": "ABC-123"},
        {"tipo": "placa", "valor": "XYZ987"},
        {"tipo": "placa", "valor": "AAA00C"},
        {"tipo": "placa", "valor": "AAA-00C"},
        {"tipo": "fecha", "valor": "26-05-2026"},
    ]
    assert analizar_texto_fsm(texto) == esperado
    assert analizar_texto_regex(texto) == esperado
