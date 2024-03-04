import requests

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

def get_next_holiday(country_code: str = current_country) -> dict:
    """Obtiene la próxima fecha festiva en un país específico.
    Args:
        country_code (str): Código de país ISO 3166-1 alfa-2.
    Returns:
        str: Próxima fecha festiva.
    """
    try:
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

