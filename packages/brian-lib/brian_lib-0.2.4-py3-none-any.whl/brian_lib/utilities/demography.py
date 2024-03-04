import requests
from datetime import datetime

def get_current_demo_data():
    """Obtiene los datos demográficos basado en la dirección IP del usuario.
    Returns:
        dict: Datos demográficos actuales.
    """
    try:
        # Hacer una solicitud a la API de ipinfo.io para obtener información sobre la IP actual
        response = requests.get('https://ipinfo.io/json')
        data = response.json()

        if data:
            return data
        
        return {"error": "No se pudo determinar los datos demográficos actuales."}
    except Exception as e:
        print("Error al obtener los datos demográficos:", e)
        return {"error": "No se pudo determinar los datos demográficos actuales."}

demo_data = get_current_demo_data()

current_country = demo_data.get('country', 'CL')
current_ip = demo_data.get('ip', '0.0.0.0')
current_city = demo_data.get('city', 'Santiago')
current_timezone = demo_data.get('timezone', 'America/Santiago')
current_location = demo_data.get('loc', '-33.4569,-70.6483')
current_lat = float(current_location.split(',')[0])
current_lon = float(current_location.split(',')[1])

def get_holidays(country_code: str = current_country, year: int = None) -> list:
    """Obtiene las fechas festivas en un país específico.
    Args:
        country_code (str): Código de país ISO 3166-1 alfa-2.
        year (int): Año para el que se desean obtener las fechas festivas.
    Returns:
        list: Fechas festivas.
    """
    try:
        if year is None:
            year = datetime.now().year
        print(f"Getting holidays for country code {country_code}")
        # Hacer una solicitud a la API de holidays para obtener las fechas festivas
        response = requests.get(f'https://date.nager.at/Api/v2/PublicHolidays/{year}/{country_code}')
        data = response.json()

        if data:
            return list(data)
        
        return list([{ "error": "No se pudieron determinar las fechas festivas."}])
    except Exception as e:
        print("Error al obtener las fechas festivas:", e)

        return list([{ "error": "No se pudieron determinar las fechas festivas."}])

def is_holiday(date: datetime = None, country_code: str = current_country, city = None) -> bool:
    """Determina si una fecha específica es festiva en un país específico.
    Args:
        country_code (str): Código de país ISO 3166-1 alfa-2.
        date (str): Fecha a verificar si es festiva.
    Returns:
        bool: True si la fecha es festiva, False si no.
    """
    holidays = get_holidays(country_code)
    if holidays:
        for holiday in holidays:
            fecha = datetime.strptime(holiday['date'],'%Y-%m-%d')
            if fecha == date:
                print(f"{holiday['date']} is a holiday in {country_code} ({holiday['localName']})")
                if not holiday['global']:
                    print('--------------------------------------------------------------')
                    print(f"La fecha festiva {holiday['localName']} no aplica a todo el país.")
                    print(f"Se aplica solo a las siguientes regiones: {', '.join(holiday['counties'])}")
                    if city is not None:
                        print(f"La ciudad actual es {city}.")
                        print('--------------------------------------------------------------')
                        return city in holiday['counties']
                    else:
                        return True
                return True
    
    return False

def get_next_holiday(country_code: str = current_country) -> dict:
    """Obtiene la próxima fecha festiva en un país específico.
    Args:
        country_code (str): Código de país ISO 3166-1 alfa-2.
    Returns:
        str: Próxima fecha festiva.
    """
    try:
        print(f"Getting next holiday for country code {country_code}")
        # Hacer una solicitud a la API de holidays para obtener la próxima fecha festiva
        response = requests.get(f'https://date.nager.at/Api/v2/NextPublicHolidays/{country_code}')
        data = response.json()

        if data:
            retorno = {'date': data[0]['date'], 
                       'name': data[0]['localName'], 
                       'global': data[0]['global']}
            retorno['cities'] = data[0]['counties'] if 'counties' in data[0] else []
            return retorno
        
        return {"error": "No se pudo determinar la próxima fecha festiva."}
    except Exception as e:
        print("Error al obtener la próxima fecha festiva:", e)

        return {"error": "No se pudo determinar la próxima fecha festiva."}

