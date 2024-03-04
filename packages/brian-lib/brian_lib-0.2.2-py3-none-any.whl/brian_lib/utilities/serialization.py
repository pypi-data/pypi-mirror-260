import json

def serialize_to_json(obj: object) -> str:
    return json.dumps(obj)

def deserialize_from_json(json_str: str) -> object:
    return json.loads(json_str)



"""
Serialización Básica:

Convertir objetos a strings (generalmente en formatos como JSON, XML, etc.).
Convertir strings de vuelta a objetos.
Serialización Binaria:

Convertir objetos a una representación binaria.
Deserializar desde una representación binaria a objetos.
Compresión:

Comprimir datos serializados para ahorrar espacio o ancho de banda.
Descomprimir datos.
Serialización Personalizada:

Serializar solo partes específicas de un objeto o estructura de datos.
Aplicar transformaciones durante la serialización/deserialización (por ejemplo, encriptación).
Serialización para Almacenamiento:

Serializar objetos para guardarlos en bases de datos.
Deserializar objetos desde bases de datos.
Conversión de Formatos:

Convertir entre diferentes formatos de serialización (por ejemplo, de JSON a XML).
Serialización Segura:

Sanitizar datos antes de la serialización para evitar vulnerabilidades (por ejemplo, ataques de inyección).
Versionado:

Añadir versiones a los datos serializados para facilitar las actualizaciones y la compatibilidad hacia atrás.
Deserializar datos de versiones anteriores.
Serialización de Tipos Específicos:

Serializar tipos específicos como arrays, matrices, gráficos, etc.
Deserializar en tipos específicos.
Validación:

Validar datos antes de la deserialización para asegurarse de que estén en el formato correcto y sean seguros.
Registro (Logging):

Registrar información sobre los procesos de serialización y deserialización.
Optimización:

Optimizar el proceso de serialización para velocidad o tamaño mínimo.
Integración con Esquemas:

Serializar/deserializar basándose en esquemas o definiciones (por ejemplo, usando Apache Avro o Protocol Buffers).
Serialización de Objetos Complejos:

Gestionar referencias circulares o repetidas en estructuras de datos.
Serializar objetos con métodos y estado interno."""