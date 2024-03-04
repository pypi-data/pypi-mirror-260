import logging
import time

logging.basicConfig(level=logging.INFO)

def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Corriendo '{func.__name__}' con args {args} y kwargs {kwargs}")
        return func(*args, **kwargs)
    return wrapper


def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"'{func.__name__}' tomo {end_time - start_time:.5f} segundos.")
        return result
    return wrapper


def retry(max_retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}. Retrying...")
            raise Exception(f"Failed after {max_retries} retries.")
        return wrapper
    return decorator


def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in '{func.__name__}': {e}")
            raise
    return wrapper

""""
OTROS POSIBLES DECORADORES....

Autorización y Autenticación:
Asegurar que un usuario esté autenticado antes de ejecutar una función.
Verificar roles o permisos antes de permitir el acceso a una función.

Conversión de tipos:
Convertir los argumentos de entrada o la salida de una función. Por ejemplo, convertir automáticamente entradas de string a números o formatos específicos.

Validación:
Verificar que los argumentos de una función cumplan con ciertos criterios antes de ejecutarla.

Registro detallado (Auditoría):
Guardar un registro detallado de cuándo se llama a una función, con qué argumentos y cuál fue el resultado.

Limitación de tasa (Rate Limiting):
Limitar cuántas veces se puede llamar a una función en un período determinado.

Singleton:
Asegurar que una clase solo tenga una instancia.

Sincronización:
Asegurar que una función solo pueda ser accedida por un hilo a la vez (útil en programación concurrente).

Deprecación:
Emitir una advertencia si se llama a una función que está marcada como obsoleta.

Timeout:
Terminar una función si su ejecución toma demasiado tiempo.

Transformaciones post-proceso:
Aplicar una transformación al resultado de una función antes de devolverlo. Por ejemplo, cambiar el formato de salida.

Argumentos por defecto:
Proporcionar valores por defecto para algunos argumentos si no se especifican.

Tracing:
Registrar un rastro de las llamadas a funciones para depurar o para análisis de rendimiento.

Notificación:
Enviar una notificación (correo electrónico, mensaje, etc.) cuando se llama a una función bajo ciertas condiciones.

Monitoreo y métricas:
Registrar métricas específicas (como el uso de recursos, contadores) cada vez que se ejecuta una función.

Enriquecimiento de contexto:
Añadir información contextual a una función (por ejemplo, información de la solicitud en una aplicación web).
"""