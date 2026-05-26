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
    """Valida fechas en formato DD/MM/AAAA o DD-MM-AAAA usando una FSM pura caracter por caracter, admitiendo parentesis."""
    if not fecha:
        return False

    # Validar que los paréntesis estén balanceados
    abiertos = 0
    for c in fecha:
        if c == "(":
            abiertos += 1
        elif c == ")":
            abiertos -= 1
            if abiertos < 0:
                return False
    if abiertos != 0:
        return False

    fecha_limpia = "".join(c for c in fecha if c not in ["(", ")"])
    if len(fecha_limpia) != 10:
        return False

    estado = "q0"
    sep_encontrado = None
    
    d1, d2 = "", ""
    m1, m2 = "", ""
    y1, y2, y3, y4 = "", "", "", ""

    for char in fecha_limpia:
        if estado == "q0":
            if _es_digito_ascii(char):
                d1 = char
                estado = "q_d1"
            else:
                return False
        elif estado == "q_d1":
            if _es_digito_ascii(char):
                d2 = char
                estado = "q_d2"
            else:
                return False
        elif estado == "q_d2":
            if char in ["/", "-"]:
                sep_encontrado = char
                estado = "q_s1"
            else:
                return False
        elif estado == "q_s1":
            if _es_digito_ascii(char):
                m1 = char
                estado = "q_m1"
            else:
                return False
        elif estado == "q_m1":
            if _es_digito_ascii(char):
                m2 = char
                estado = "q_m2"
            else:
                return False
        elif estado == "q_m2":
            if char == sep_encontrado:
                estado = "q_s2"
            else:
                return False
        elif estado == "q_s2":
            if _es_digito_ascii(char):
                y1 = char
                estado = "q_y1"
            else:
                return False
        elif estado == "q_y1":
            if _es_digito_ascii(char):
                y2 = char
                estado = "q_y2"
            else:
                return False
        elif estado == "q_y2":
            if _es_digito_ascii(char):
                y3 = char
                estado = "q_y3"
            else:
                return False
        elif estado == "q_y3":
            if _es_digito_ascii(char):
                y4 = char
                estado = "q_y4"
            else:
                return False
        else:
            return False

    if estado != "q_y4":
        return False

    # Ahora validamos los valores reales de fecha con calendario
    dia = int(d1 + d2)
    mes = int(m1 + m2)
    anio = int(y1 + y2 + y3 + y4)

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
    """Valida teléfonos en Colombia usando un DFA estructurado y determinista (sin bucles infinitos de separadores)."""
    if not telefono:
        return False

    estado = "q0"

    for char in telefono:
        if estado == "q0":
            if char == "+":
                estado = "qp1"
            elif char == "(":
                estado = "q_p3_1"
            elif char == "3":
                estado = "qd1"
            else:
                return False
        elif estado == "qp1":
            if char == "5":
                estado = "qp2"
            else:
                return False
        elif estado == "qp2":
            if char == "7":
                estado = "qp3"
            else:
                return False
        elif estado == "qp3":
            if char == " ":
                estado = "qp3_space"
            elif char == "(":
                estado = "q_p3_1"
            elif char == "3":
                estado = "qd1"
            else:
                return False
        elif estado == "qp3_space":
            if char == "(":
                estado = "q_p3_1"
            elif char == "3":
                estado = "qd1"
            else:
                return False
        elif estado == "q_p3_1":
            if char == "3":
                estado = "qd1_p"
            else:
                return False
        elif estado == "qd1_p":
            if _es_digito_ascii(char):
                estado = "qd2_p"
            else:
                return False
        elif estado == "qd2_p":
            if _es_digito_ascii(char):
                estado = "qd3_p"
            else:
                return False
        elif estado == "qd3_p":
            if char == ")":
                estado = "qd3"
            else:
                return False
        elif estado == "qd1":
            if _es_digito_ascii(char):
                estado = "qd2"
            else:
                return False
        elif estado == "qd2":
            if _es_digito_ascii(char):
                estado = "qd3"
            else:
                return False
        elif estado == "qd3":
            if char in [" ", "-", "."]:
                estado = "q_sep1"
            elif _es_digito_ascii(char):
                estado = "qd4"
            else:
                return False
        elif estado == "q_sep1":
            if _es_digito_ascii(char):
                estado = "qd4"
            else:
                return False
        elif estado == "qd4":
            if _es_digito_ascii(char):
                estado = "qd5"
            else:
                return False
        elif estado == "qd5":
            if _es_digito_ascii(char):
                estado = "qd6"
            else:
                return False
        elif estado == "qd6":
            if char in [" ", "-", "."]:
                estado = "q_sep2"
            elif _es_digito_ascii(char):
                estado = "qd7"
            else:
                return False
        elif estado == "q_sep2":
            if _es_digito_ascii(char):
                estado = "qd7"
            else:
                return False
        elif estado == "qd7":
            if _es_digito_ascii(char):
                estado = "qd8"
            else:
                return False
        elif estado == "qd8":
            if char in [" ", "-", "."]:
                estado = "q_sep3"
            elif _es_digito_ascii(char):
                estado = "qd9"
            else:
                return False
        elif estado == "q_sep3":
            if _es_digito_ascii(char):
                estado = "qd9"
            else:
                return False
        elif estado == "qd9":
            if _es_digito_ascii(char):
                estado = "qd10"
            else:
                return False
        elif estado == "qd10":
            return False  # No se permiten más caracteres después del décimo dígito
        else:
            return False

    return estado == "qd10"


def validar_url(url: str) -> bool:
    """Valida URLs basadas en http o https, soportando localhost, dominios estándar o IPs (octetos <= 255)."""
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

    # Comprobar si es dirección IP (4 octetos numéricos entre 0 y 255)
    partes_ip = host.split(".")
    es_ip = len(partes_ip) == 4 and all(p.isdigit() for p in partes_ip)
    if es_ip:
        for part in partes_ip:
            val = int(part)
            if val < 0 or val > 255:
                return False
            # Evitar ceros a la izquierda innecesarios (ej: 01)
            if len(part) > 1 and part[0] == "0":
                return False
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
    """Valida placas en formato LLL-000, LLL000, LLL-00L o LLL00L."""
    if not placa:
        return False

    valor = placa.strip().upper()

    if len(valor) == 7 and valor[3] == "-":
        letras = valor[0:3]
        sufijo = valor[4:7]
    elif len(valor) == 6:
        letras = valor[0:3]
        sufijo = valor[3:6]
    else:
        return False

    for ch in letras:
        if not _es_letra_ascii(ch):
            return False

    # Dos primeros deben ser dígitos
    if not (_es_digito_ascii(sufijo[0]) and _es_digito_ascii(sufijo[1])):
        return False

    # Último puede ser dígito (LLL000) o letra (LLL00L)
    ultimo = sufijo[2]
    if _es_digito_ascii(ultimo) or _es_letra_ascii(ultimo):
        return True

    return False


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
