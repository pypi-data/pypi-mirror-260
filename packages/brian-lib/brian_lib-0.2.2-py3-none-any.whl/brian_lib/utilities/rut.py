from itertools import cycle

def validate_rut_format(rut: str) -> bool:
    """Valida si un número de RUT dado es válido, verificando su estructura y su dígito verificador según el algoritmo correspondiente.
    Args:
        rut (str): Número de RUT a validar.
    Returns:
        bool: True si el RUT es válido, False si no.
    """
    try:
        rut = rut.replace('.', '').replace('-', '')
        if len(rut) < 2:
            return False
        rut, dv = rut[:-1], rut[-1]
        reversed_digits = map(int, reversed(str(rut)))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_digits, factors))
        return dv == str((11 - s % 11) % 11)
    except Exception as e:
        print("Error al validar el RUT:", e)
        return False

def generate_rut_dv(rut: str) -> str:
    """Genera el dígito verificador correspondiente para un número de RUT dado, siguiendo el algoritmo específico.
    Args:
        rut (str): Número de RUT al que se le generará el dígito verificador.
    Returns:
        str: Dígito verificador generado.
    """
    try:
        rut = rut.replace('.', '').replace('-', '')
        reversed_digits = map(int, reversed(str(rut)))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_digits, factors))
        return str((11 - s % 11) % 11)
    except Exception as e:
        print("Error al generar el dígito verificador del RUT:", e)
        return ""

def format_rut(rut: str) -> str:
    """Formatea un número de RUT para presentarlo de manera legible, añadiendo puntos y guiones según el formato comúnmente utilizado.
    Args:
        rut (str): Número de RUT a formatear.
    Returns:
        str: RUT formateado.
    """
    try:
        rut = rut.replace('.', '').replace('-', '')
        return f"{rut[:-7]}.{rut[-7:-4]}.{rut[-4:-1]}-{rut[-1]}"
    except Exception as e:
        print("Error al formatear el RUT:", e)
        return rut

def get_rut_number(rut: str) -> str:
    """Extrae el número base de un RUT, sin incluir el dígito verificador.
    Args:
        rut (str): Número de RUT del que se extraerá el número base.
    Returns:
        str: Número base del RUT.
    """
    try:
        return rut.replace('.', '').replace('-', '')[:-1]
    except Exception as e:
        print("Error al obtener el número base del RUT:", e)
        return rut

def get_rut_dv(rut: str) -> str:
    """Extrae el dígito verificador de un RUT.
    Args:
        rut (str): Número de RUT del que se extraerá el dígito verificador.
    Returns:
        str: Dígito verificador del RUT.
    """
    try:
        return rut.replace('.', '').replace('-', '')[-1]
    except Exception as e:
        print("Error al obtener el dígito verificador del RUT:", e)
        return ""

def normalize_rut(rut: str) -> str:
    """Normaliza un número de RUT eliminando caracteres especiales y convirtiéndolo a un formato estándar.
    Args:
        rut (str): Número de RUT a normalizar.
    Returns:
        str: RUT normalizado.
    """
    try:
        return rut.replace('.', '').replace('-', '').upper()
    except Exception as e:
        print("Error al normalizar el RUT:", e)
        return rut

def generate_random_rut() -> str:
    """Genera un número de RUT aleatorio válido.
    Returns:
        str: RUT aleatorio generado.
    """
    try:
        import random
        number = str(random.randint(1000000, 25000000))
        return format_rut(f"{number}-{generate_rut_dv(number)}")
    except Exception as e:
        print("Error al generar un RUT aleatorio:", e)
        return ""

