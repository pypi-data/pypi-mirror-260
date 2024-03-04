from datetime import datetime, timedelta
import pytz
import ephem

from .demography import current_country, current_timezone, current_lat, current_lon, is_holiday

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATE_TIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'


def get_date_time(format: str=DATE_TIME_FORMAT) -> str:
    """Obtiene la fecha y hora actuales.
    Args:
        format (str, optional): Formato de la fecha y hora. Defaults to '%Y-%m-%d %H:%M:%S'.
    Returns:
        str: Fecha y hora actuales.
    """
    return datetime.now().strftime(format)


def get_date(format: str=DATE_FORMAT) -> str:
    """Obtiene solo la fecha actual.
    Args:
        format (str, optional): Formato de la fecha. Defaults to '%Y-%m-%d'.
    Returns:
        str: Fecha actual.
    """
    return datetime.now().strftime(format)


def get_time(format: str=TIME_FORMAT) -> str:
    """Obtiene solo la hora actual.
    Args:
        format (str, optional): Formato de la hora. Defaults to '%H:%M:%S'.
    Returns:
        str: Hora actual.
    """
    return datetime.now().strftime(format)


def format_date_time(date_time: datetime, format: str=DATE_TIME_FORMAT) -> str:
    """Convierte una fecha y hora a una cadena de texto con un formato específico.
    Args:
        date_time (datetime): Fecha y hora a formatear.
        format (str, optional): Formato de la fecha y hora. Defaults to '%Y-%m-%d %H:%M:%S'.
    Returns:
        str: Fecha y hora formateada.
    """
    return date_time.strftime(format)


def format_date(date: datetime, format: str=DATE_FORMAT) -> str:
    """Formatea la fecha en diversos estilos.
    Args:
        date (datetime): Fecha a formatear.
        format (str, optional): Formato de la fecha. Defaults to '%Y-%m-%d'.
    Returns:
        str: Fecha formateada.
    """
    return date.strftime(format)


def format_time(time: datetime, format: str=TIME_FORMAT) -> str:
    """Formatea la hora en diversos estilos.
    Args:
        time (datetime): Hora a formatear.
        format (str, optional): Formato de la hora. Defaults to '%H:%M:%S'.
    Returns:
        str: Hora formateada.
    """
    return time.strftime(format)


def str_to_date_time(date_time: str, format: str=DATE_TIME_FORMAT) -> datetime:
    """Convierte una cadena de texto a un objeto de fecha y hora.
    Args:
        date_time (str): Fecha y hora a convertir.
        format (str, optional): Formato de la fecha y hora. Defaults to '%Y-%m-%d %H:%M:%S'.
    Returns:
        datetime: Fecha y hora convertida.
    """
    return datetime.strptime(date_time, format)


def str_to_date(date: str, format: str=DATE_FORMAT) -> datetime:
    """Convierte una cadena de texto a un objeto de fecha.
    Args:
        date (str): Fecha a convertir.
        format (str, optional): Formato de la fecha. Defaults to '%Y-%m-%d'.
    Returns:
        datetime: Fecha convertida.
    """
    return datetime.strptime(date, format)


def str_to_time(time: str, format: str=TIME_FORMAT) -> datetime:
    """Convierte una cadena de texto a un objeto de hora.
    Args:
        time (str): Hora a convertir.
        format (str, optional): Formato de la hora. Defaults to '%H:%M:%S'.
    Returns:
        datetime: Hora convertida.
    """
    return datetime.strptime(time, format)


def add_days(date_time: datetime, days: int) -> datetime:
    """Añade o sustrae días a una fecha y hora dada.
    Args:
        date_time (datetime): Fecha y hora a modificar.
        days (int): Días a añadir o sustraer.
    Returns:
        datetime: Fecha y hora modificada.
    """
    return date_time + timedelta(days=days)


def add_months(date_time: datetime, months: int) -> datetime:
    """Añade o sustrae meses a una fecha y hora dada.
    Args:
        date_time (datetime): Fecha y hora a modificar.
        months (int): Meses a añadir o sustraer.
    Returns:
        datetime: Fecha y hora modificada.
    """
    return date_time + timedelta(days=months*30)


def add_years(date_time: datetime, years: int) -> datetime:
    """Añade o sustrae años a una fecha y hora dada.
    Args:
        date_time (datetime): Fecha y hora a modificar.
        years (int): Años a añadir o sustraer.
    Returns:
        datetime: Fecha y hora modificada.
    """
    return date_time + timedelta(days=years*365)


def add_hours(date_time: datetime, hours: int) -> datetime:
    """Añade o sustrae horas a una fecha y hora dada.
    Args:
        date_time (datetime): Fecha y hora a modificar.
        hours (int): Horas a añadir o sustraer.
    Returns:
        datetime: Fecha y hora modificada.
    """
    return date_time + timedelta(hours=hours)


def add_minutes(date_time: datetime, minutes: int) -> datetime:
    """Añade o sustrae minutos a una fecha y hora dada.
    Args:
        date_time (datetime): Fecha y hora a modificar.
        minutes (int): Minutos a añadir o sustraer.
    Returns:
        datetime: Fecha y hora modificada.
    """
    return date_time + timedelta(minutes=minutes)


def add_seconds(date_time: datetime, seconds: int) -> datetime:
    """Añade o sustrae segundos a una fecha y hora dada.
    Args:
        date_time (datetime): Fecha y hora a modificar.
        seconds (int): Segundos a añadir o sustraer.
    Returns:
        datetime: Fecha y hora modificada.
    """
    return date_time + timedelta(seconds=seconds)


def get_days_between(date1: datetime, date2: datetime) -> int:
    """Calcula la diferencia entre dos fechas.
    Args:
        date1 (datetime): Primera fecha.
        date2 (datetime): Segunda fecha.
    Returns:
        int: Diferencia en días.
    """
    return (date1 - date2).days


def get_gmt_offset() -> int:
    """Obtiene el desplazamiento horario de la hora actual.
    Returns:
        int: Desplazamiento horario.
    """
    return datetime.now().astimezone().utcoffset() // timedelta(hours=1)


def get_timezones() -> list:
    """Obtiene una lista de zonas horarias disponibles.
    Returns:
        list: Zonas horarias disponibles.
    """
    return pytz.all_timezones


def get_timezone() -> str:
    """Obtiene la zona horaria actual.
    Returns:
        str: Zona horaria actual.
    """
    return current_timezone if current_timezone in get_timezones() else 'America/Santiago'


def convert_timezone(date_time: datetime, timezone: str) -> datetime:
    """Convierte una fecha y hora entre diferentes zonas horarias.
    Args:
        date_time (datetime): Fecha y hora a convertir.
        timezone (str): Zona horaria de destino.
    Returns:
        datetime: Fecha y hora convertida.
    """
    if timezone not in get_timezones():
        raise ValueError('Zona horaria no válida.')
    return date_time.astimezone(pytz.timezone(timezone))


def is_leap_year(year: int = None) -> bool:
    """Verifica si un año es bisiesto.
    Args:
        year (int): Año a verificar.
    Returns:
        bool: True si es bisiesto, False en caso contrario.
    """
    if year is None:
        year = datetime.now().year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_weekday(date: datetime) -> str:
    """Obtiene el día de la semana para una fecha dada.
    Args:
        date (datetime): Fecha a verificar.
    Returns:
        str: Día de la semana.
    """
    return date.strftime('%A')


def get_weekday_number(date: datetime) -> int:
    """Obtiene el número del día de la semana para una fecha dada.
    Args:
        date (datetime): Fecha a verificar.
    Returns:
        int: Número del día de la semana.
    """
    return date.weekday()


def is_valid_date_time(date_time: str, format: str='%Y-%m-%d %H:%M:%S') -> bool:
    """Valida si una cadena es una fecha y hora válida según un formato específico.
    Args:
        date_time (str): Fecha y hora a validar.
        format (str, optional): Formato de la fecha y hora. Defaults to '%Y-%m-%d %H:%M:%S'.
    Returns:
        bool: True si es válida, False en caso contrario.
    """
    try:
        datetime.strptime(date_time, format)
        return True
    except ValueError:
        return False


def compare_dates(date1: datetime, date2: datetime) -> int:
    """Compara dos fechas u horas para determinar cuál es anterior o posterior.
    Args:
        date1 (datetime): Primera fecha.
        date2 (datetime): Segunda fecha.
    Returns:
        int: -1 si date1 < date2, 0 si date1 == date2, 1 si date1 > date2.
    """
    if date1 < date2:
        return -1
    elif date1 > date2:
        return 1
    else:
        return 0


def get_mayor_date(date1: datetime, date2: datetime) -> datetime:
    """Obtiene la fecha mayor entre dos fechas dadas.
    Args:
        date1 (datetime): Primera fecha.
        date2 (datetime): Segunda fecha.
    Returns:
        datetime: Fecha mayor.
    """
    return date1 if date1 > date2 else date2


def is_equal_date(date1: datetime, date2: datetime) -> bool:
    """Verifica si dos fechas son iguales.
    Args:
        date1 (datetime): Primera fecha.
        date2 (datetime): Segunda fecha.
    Returns:
        bool: True si son iguales, False en caso contrario.
    """
    return date1 == date2


def is_summer_time(date: datetime, timezone: str = get_timezone()) -> bool:
    """Verifica si una fecha y hora se encuentra en horario de verano.
    Args:
        date (datetime): Fecha y hora a verificar.
    Returns:
        bool: True si es horario de verano, False en caso contrario.
    """
    return bool(pytz.timezone(timezone).dst(date))


def get_timezone_by_location(country: str = current_country) -> str:
    """Obtiene la zona horaria de una ubicación geográfica.
    Args:
        latitude (float): Latitud de la ubicación.
        longitude (float): Longitud de la ubicación.
    Returns:
        str: Zona horaria de la ubicación.
    """
    return pytz.timezone(pytz.country_timezones(country)[0]).tzname(datetime.now())


def get_sunrise_sunset(latitude: float = current_lat, longitude: float = current_lon, date: datetime = datetime.utcnow()) -> tuple:
    """Calcula la hora del amanecer y el atardecer para una ubicación y fecha dadas.
    Args:
        latitude (float): Latitud de la ubicación.
        longitude (float): Longitud de la ubicación.
        date (datetime): Fecha a verificar.
    Returns:
        tuple: Hora del amanecer y el atardecer en la zona horaria local.
    """

    if latitude is None or longitude is None or date is None:
        raise ValueError("Se deben proporcionar valores para latitud, longitud y fecha.")
    
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.date = date

    sun = ephem.Sun()

    sunrise_utc = observer.previous_rising(sun).datetime()
    sunset_utc = observer.next_setting(sun).datetime()

    return add_hours(sunrise_utc, get_gmt_offset()), add_hours(sunset_utc, get_gmt_offset())


def get_duration(date1: datetime, date2: datetime) -> str:
    """Obtiene la duración entre dos fechas.
    Args:
        date1 (datetime): Primera fecha.
        date2 (datetime): Segunda fecha.
    Returns:
        str: Duración entre las fechas.
    """
    duration = date1 - date2
    return str(duration)


def date_to_timestamp(date: datetime) -> int:
    """Convierte una fecha a un timestamp.
    Args:
        date (datetime): Fecha a convertir.
    Returns:
        int: Timestamp.
    """
    return int(date.timestamp())


def timestamp_to_date(timestamp: int) -> datetime:
    """Convierte un timestamp a una fecha.
    Args:
        timestamp (int): Timestamp a convertir.
    Returns:
        datetime: Fecha.
    """
    return datetime.fromtimestamp(timestamp)

def is_business_day(date: datetime = None, country_code: str = None, city: str = None) -> bool:
    """Determina si una fecha es un día hábil.
    Args:
        date (datetime): Fecha a verificar.
    Returns:
        bool: True si es un día hábil, False si no.
    """
    if country_code is None:
        country_code = current_country
    if date is None:
        date = datetime.now()
    if date.weekday() > 4:
        print('Es fin de semana')
        return False
    if is_holiday(date=date, country_code=country_code, city=city):
        print('Es festivo')
        return False
    return True


"""
TODO:

Timestamps (Marcas de Tiempo):
Convertir entre fechas y timestamps.
Obtener el timestamp actual.

Reloj y Alarmas:
Establecer alarmas o recordatorios para un momento específico.
Medir intervalos de tiempo (cronómetro).

Eventos Recurrentes:
Determinar las fechas de eventos que ocurren regularmente (por ejemplo, "el primer lunes de cada mes").
Calcular fechas de aniversarios o eventos anuales.

Internacionalización (i18n):
Localizar la representación de fechas y horas para diferentes culturas o idiomas.

Historial de Fechas:
Almacenar y recuperar fechas importantes o eventos históricos.
"""