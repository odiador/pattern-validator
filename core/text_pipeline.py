from typing import List, Dict

from core.automata_core import (
    validar_correo,
    validar_fecha,
    validar_telefono,
    validar_url,
    validar_placa,
)


def _tokenizar_candidatos(texto: str) -> List[str]:
    if not texto:
        return []

    permitidos = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "@._-+/:?&=#()[]"
    )

    tokens: List[str] = []
    actual: List[str] = []

    for ch in texto:
        if ch in permitidos:
            actual.append(ch)
        else:
            if actual:
                tokens.append("".join(actual))
                actual = []
    if actual:
        tokens.append("".join(actual))

    return tokens


def _limpiar_token(token: str) -> str:
    if not token:
        return ""
    return token.strip(".,;:!?()[]{}<>\"'")


def analizar_texto(texto: str) -> List[Dict[str, str]]:
    """Extrae patrones validos desde un bloque de texto."""
    candidatos = _tokenizar_candidatos(texto)
    resultados: List[Dict[str, str]] = []
    vistos = set()

    # Se ordenan de más específico a más general para evitar ambigüedades.
    # El teléfono es el más permisivo, por lo que se evalúa al final.
    validadores = [
        ("fecha", validar_fecha),
        ("url", validar_url),
        ("correo", validar_correo),
        ("placa", validar_placa),
        ("telefono", validar_telefono),
    ]

    for candidato in candidatos:
        valor = _limpiar_token(candidato)
        if not valor:
            continue
        for nombre, validador in validadores:
            if validador(valor):
                clave = (nombre, valor)
                if clave not in vistos:
                    resultados.append({"tipo": nombre, "valor": valor})
                    vistos.add(clave)
                # Una vez que el token coincide con un patrón específico,
                # no debe ser procesado por otros validadores.
                break

    return resultados
