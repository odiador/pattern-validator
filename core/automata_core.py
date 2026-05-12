def _es_letra_ascii(char: str) -> bool:
    return ("a" <= char <= "z") or ("A" <= char <= "Z")


def _es_digito_ascii(char: str) -> bool:
    return "0" <= char <= "9"


def _es_alnum_ascii(char: str) -> bool:
    return _es_letra_ascii(char) or _es_digito_ascii(char)


def validar_correo(correo: str) -> bool:
    """Valida un correo usando FSM sin regex."""
    if not correo:
        return False

    estado = "q0"
    tld_len = 0

    for char in correo:
        if estado == "q0":
            if _es_alnum_ascii(char):
                estado = "q1"
            else:
                return False
        elif estado == "q1":
            if _es_alnum_ascii(char) or char in [".", "_", "-"]:
                continue
            if char == "@":
                estado = "q2"
            else:
                return False
        elif estado == "q2":
            if _es_alnum_ascii(char):
                estado = "q3"
            else:
                return False
        elif estado == "q3":
            if _es_alnum_ascii(char) or char == "-":
                continue
            if char == ".":
                estado = "q4"
                tld_len = 0
            else:
                return False
        elif estado == "q4":
            if _es_letra_ascii(char):
                estado = "q5"
                tld_len = 1
            else:
                return False
        elif estado == "q5":
            if _es_letra_ascii(char):
                tld_len += 1
                continue
            if char == ".":
                if tld_len < 2:
                    return False
                estado = "q4"
                tld_len = 0
            else:
                return False

    return estado == "q5" and tld_len >= 2


def validar_fecha(fecha: str) -> bool:
    """Valida fechas en formato DD/MM/AAAA o DD-MM-AAAA."""
    if not fecha or len(fecha) != 10:
        return False

    sep = fecha[2]
    if sep not in ["/", "-"]:
        return False
    if fecha[5] != sep:
        return False

    for idx in [0, 1, 3, 4, 6, 7, 8, 9]:
        if not _es_digito_ascii(fecha[idx]):
            return False

    dia = int(fecha[0:2])
    mes = int(fecha[3:5])
    anio = int(fecha[6:10])

    if mes < 1 or mes > 12:
        return False
    if dia < 1:
        return False

    def es_bisiesto(valor: int) -> bool:
        return (valor % 4 == 0 and valor % 100 != 0) or (valor % 400 == 0)

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if mes == 2 and es_bisiesto(anio):
        dias_por_mes[1] = 29

    return dia <= dias_por_mes[mes - 1]


def validar_telefono(telefono: str) -> bool:
    """Valida telefonos con digitos y separadores comunes."""
    if not telefono:
        return False

    estado = "start"
    total_digitos = 0
    separadores = [" ", "-", ".", "(", ")"]

    for char in telefono:
        if estado == "start":
            if char == "+":
                estado = "plus"
            elif char == "(":
                estado = "sep"
            elif _es_digito_ascii(char):
                total_digitos += 1
                estado = "digits"
            else:
                return False
        elif estado == "plus":
            if _es_digito_ascii(char):
                total_digitos += 1
                estado = "digits"
            elif char == "(":
                estado = "sep"
            else:
                return False
        elif estado == "digits":
            if _es_digito_ascii(char):
                total_digitos += 1
            elif char in separadores:
                estado = "sep"
            else:
                return False
        elif estado == "sep":
            if _es_digito_ascii(char):
                total_digitos += 1
                estado = "digits"
            elif char in separadores:
                continue
            else:
                return False

    return (estado == "digits" or estado == "sep") and 7 <= total_digitos <= 15


def validar_url(url: str) -> bool:
    """Valida URLs basadas en http o https."""
    if not url:
        return False

    if url.startswith("https://"):
        resto = url[8:]
    elif url.startswith("http://"):
        resto = url[7:]
    else:
        return False

    if not resto or " " in resto:
        return False

    dominio_completo, _, ruta = resto.partition("/")
    if not dominio_completo:
        return False

    host = dominio_completo
    puerto = None
    if ":" in dominio_completo:
        host, puerto_str = dominio_completo.split(":", 1)
        if not puerto_str.isdigit():
            return False
        if not (1 <= int(puerto_str) <= 65535):
            return False

    if not host:
        return False

    if host == "localhost":
        return True

    if "." not in host:
        return False

    def etiqueta_valida(etiqueta: str) -> bool:
        if not etiqueta:
            return False
        if etiqueta[0] == "-" or etiqueta[-1] == "-":
            return False
        for ch in etiqueta:
            if not (_es_alnum_ascii(ch) or ch == "-"):
                return False
        return True

    etiquetas = host.split(".")
    for etq in etiquetas:
        if not etiqueta_valida(etq):
            return False

    tld = etiquetas[-1]
    if len(tld) < 2 or len(tld) > 24:
        return False
    for ch in tld:
        if not _es_letra_ascii(ch):
            return False

    return True


def validar_placa(placa: str) -> bool:
    """Valida placas en formato LLL-000 o LLL000."""
    if not placa:
        return False

    valor = placa.strip()
    if len(valor) == 7 and valor[3] == "-":
        letras = valor[0:3]
        numeros = valor[4:7]
    elif len(valor) == 6:
        letras = valor[0:3]
        numeros = valor[3:6]
    else:
        return False

    for ch in letras:
        if not _es_letra_ascii(ch):
            return False
    for ch in numeros:
        if not _es_digito_ascii(ch):
            return False

    return True


def validar_password(password: str) -> bool:
    """Valida contrasenas con longitud y complejidad minima."""
    if not password:
        return False
    if len(password) < 8 or len(password) > 32:
        return False

    especiales = set("!@#$%^&*()-_=+[]{};:,.?/\\|~")
    tiene_mayus = False
    tiene_minus = False
    tiene_digito = False
    tiene_especial = False

    for ch in password:
        if ch.isspace():
            return False
        if "A" <= ch <= "Z":
            tiene_mayus = True
        elif "a" <= ch <= "z":
            tiene_minus = True
        elif _es_digito_ascii(ch):
            tiene_digito = True
        elif ch in especiales:
            tiene_especial = True
        else:
            return False

    return tiene_mayus and tiene_minus and tiene_digito and tiene_especial


def aislar_correos(texto: str) -> list:
    """Tokeniza por espacios y retorna correos validos."""
    palabras = texto.split()
    correos = []

    for palabra in palabras:
        palabra = palabra.strip(".,;!?()[]{}")
        if validar_correo(palabra):
            correos.append(palabra)

    return correos
