"""Validadores y extractor basados en expresiones regulares.

Este modulo ofrece una alternativa al motor FSM (sin regex) para:
- Validar entradas de formularios
- Extraer patrones desde texto

Nota: Se sigue validando coherencia de calendario para fechas.
"""

from __future__ import annotations

from datetime import date
from typing import Dict, List

import re


_EMAIL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*@[A-Za-z0-9-]+(?:\.[A-Za-z]{2,24})+$")
_PLACA_RE = re.compile(r"^[A-Za-z]{3}-?(?:\d{3}|\d{2}[A-Za-z])$")
_PASSWORD_RE = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{8,32}$")
_FECHA_RE = re.compile(r"^(\d{2})([/-])(\d{2})\2(\d{4})$")


def validar_correo(correo: str) -> bool:
    if not correo:
        return False
    return _EMAIL_RE.fullmatch(correo.strip()) is not None


def validar_placa(placa: str) -> bool:
    if not placa:
        return False
    return _PLACA_RE.fullmatch(placa.strip()) is not None


def validar_password(password: str) -> bool:
    if not password:
        return False
    return _PASSWORD_RE.fullmatch(password) is not None


def validar_telefono(telefono: str) -> bool:
    if not telefono:
        return False

    valor = telefono.strip()
    if any(c.isalpha() for c in valor):
        return False

    # Permitimos +, espacios, guiones, puntos y parentesis.
    if re.fullmatch(r"[0-9+().\-\s]+", valor) is None:
        return False

    digitos = re.findall(r"\d", valor)
    return 7 <= len(digitos) <= 15


def validar_fecha(fecha: str) -> bool:
    if not fecha:
        return False

    m = _FECHA_RE.fullmatch(fecha.strip())
    if not m:
        return False

    d_s, _, m_s, y_s = m.groups()
    d_i = int(d_s)
    m_i = int(m_s)
    y_i = int(y_s)

    try:
        date(y_i, m_i, d_i)
    except ValueError:
        return False
    return True


def validar_url(url: str) -> bool:
    if not url:
        return False

    valor = url.strip()
    if " " in valor:
        return False

    # Soporta localhost o dominio con TLD 2-24 y puerto opcional.
    patron = (
        r"^https?://"
        r"(localhost|(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,24})"
        r"(?::\d{1,5})?"
        r"(?:/[^\s]*)?$"
    )
    if re.fullmatch(patron, valor) is None:
        return False

    # Validacion de rango de puerto si existe.
    hostport = valor.split("//", 1)[1].split("/", 1)[0]
    if ":" in hostport and not hostport.startswith("localhost"):
        host, port_s = hostport.rsplit(":", 1)
        if port_s.isdigit():
            port = int(port_s)
            if not (1 <= port <= 65535):
                return False

    return True


def analizar_texto(texto: str) -> List[Dict[str, str]]:
    """Extrae patrones validos desde un bloque de texto usando regex + validadores."""
    if not texto:
        return []

    resultados: List[Dict[str, str]] = []
    vistos = set()

    # Orden: especifico -> general (telefono al final).
    buscadores = [
        ("fecha", re.compile(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"), validar_fecha),
        ("url", re.compile(r"https?://[^\s<>\"']+"), validar_url),
        (
            "correo",
            re.compile(r"\b[A-Za-z0-9][A-Za-z0-9._-]*@[A-Za-z0-9-]+(?:\.[A-Za-z]{2,24})+\b"),
            validar_correo,
        ),
        ("placa", re.compile(r"\b[A-Za-z]{3}-?(?:\d{3}|\d{2}[A-Za-z])\b"), validar_placa),
        ("telefono", re.compile(r"\+?\d[\d\s().\-]{6,}\d"), validar_telefono),
    ]

    for tipo, patron, validador in buscadores:
        for m in patron.finditer(texto):
            valor = m.group(0).strip(".,;:!?()[]{}<>\"'")
            if not valor:
                continue
            if validador(valor):
                clave = (tipo, valor)
                if clave not in vistos:
                    resultados.append({"tipo": tipo, "valor": valor})
                    vistos.add(clave)

    return resultados
