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
    ("32/01/2024", False),
    ("29/02/2023", False),
    ("01/01/99", False),
    ("aa/bb/cccc", False),
])
def test_validar_fecha(fecha, esperado):
    assert validar_fecha(fecha) == esperado

@pytest.mark.parametrize("telefono, esperado", [
    ("+57 3123456789", True),
    ("123-4567", True),
    ("300.123.4567", True),
    ("(601) 1234567", True),
    ("123", False),
    ("abc-defg", False),
    ("+", False),
    ("1234567890123456", False),
])
def test_validar_telefono(telefono, esperado):
    assert validar_telefono(telefono) == esperado

@pytest.mark.parametrize("url, esperado", [
    ("https://google.com", True),
    ("http://localhost:8080", True),
    ("https://sub.domain.org/path?q=1", True),
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
    ("AB-123", False),
    ("ABC-12", False),
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
