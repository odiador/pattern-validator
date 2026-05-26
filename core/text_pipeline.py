from typing import List, Dict

from core.automata_core import (
    validar_correo,
    validar_fecha,
    validar_telefono,
    validar_url,
    validar_placa,
)


def _tokenizar_candidatos_con_pos(texto: str) -> List[tuple]:
    if not texto:
        return []

    permitidos = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "@._-+/:?&=#()[]"
    )

    tokens: List[tuple] = []
    actual: List[str] = []
    inicio_token = -1

    for idx, ch in enumerate(texto):
        if ch in permitidos:
            if not actual:
                inicio_token = idx
            actual.append(ch)
        else:
            if actual:
                tokens.append((inicio_token, "".join(actual)))
                actual = []
    if actual:
        tokens.append((inicio_token, "".join(actual)))

    return tokens


def _limpiar_token(token: str) -> str:
    if not token:
        return ""
    return token.strip(".,;:!?()[]{}<>\"'")


def _buscar_candidatos_telefono_con_pos(texto: str) -> List[tuple]:
    """Escanea el texto en búsqueda de secuencias contiguas que correspondan a un patrón telefónico (admitiendo espacios)."""
    candidatos = []
    n = len(texto)
    i = 0
    while i < n:
        if texto[i] in "+3(0123456789":
            inicio = i
            while i < n and (texto[i].isdigit() or texto[i] in " +-()."):
                i += 1
            candidato = texto[inicio:i].strip()
            # Limpiar posibles delimitadores colgantes al final
            while candidato and candidato[-1] in " +-.((":
                candidato = candidato[:-1]
            if candidato:
                digitos = sum(1 for c in candidato if c.isdigit())
                if digitos >= 7:
                    candidatos.append((inicio, candidato))
        else:
            i += 1
    return candidatos


def analizar_texto(texto: str) -> List[Dict[str, str]]:
    """Extrae patrones validos desde un bloque de texto en orden cronológico de aparición."""
    candidatos_con_pos = _tokenizar_candidatos_con_pos(texto) + _buscar_candidatos_telefono_con_pos(texto)
    candidatos_con_pos.sort(key=lambda x: x[0])

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

    for _, candidato in candidatos_con_pos:
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
