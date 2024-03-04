"""
Normalización y Estandarización:

Normalizar valores a un rango [0, 1].
Estandarizar valores para tener media 0 y desviación estándar 1.
Manejo de valores faltantes (NaNs):

Imputación: Rellenar valores faltantes con la media, mediana, moda o un valor constante.
Eliminar registros con valores faltantes.
Conversión de tipos de datos:

Convertir columnas de texto a números (por ejemplo, mediante codificación one-hot o etiquetado).
Convertir columnas numéricas a categorías, por ejemplo, binning.
Cambiar el tipo de datos para optimizar el uso de memoria.
Transformaciones matemáticas:

Aplicar funciones logarítmicas, exponenciales, raíz cuadrada, etc.
Calcular diferencias entre filas o columnas.
Crear combinaciones polinómicas de características.
Transformaciones temporales:

Extraer componentes de una fecha (año, mes, día, día de la semana, etc.).
Calcular diferencias de tiempo entre registros.
Resamplear series temporales.
Manipulaciones de texto:

Tokenización.
Eliminación de palabras comunes (stop words).
Stemming o lematización.
Extracción de características de texto, como n-grams.
Agregaciones y resúmenes:

Calcular sumas, promedios, máximos, mínimos, etc.
Agrupar datos y realizar agregaciones.
Reordenamiento y restructuración:

Pivotear tablas.
Fusionar o unir diferentes conjuntos de datos.
Ordenar o filtrar registros.
Transformaciones geoespaciales:

Calcular distancias entre puntos.
Convertir coordenadas entre diferentes sistemas.
Codificación y decodificación:

Codificar etiquetas en números y viceversa.
Codificación one-hot para variables categóricas.
Decodificar valores codificados.
Reducción de dimensionalidad:

PCA (Análisis de Componentes Principales).
t-SNE.
UMAP.
Balanceo de datos:

Sobremuestreo o submuestreo para equilibrar conjuntos de datos desequilibrados (por ejemplo, en problemas de clasificación).
Transformaciones específicas del dominio:

Depende del campo (por ejemplo, en finanzas, cálculo de retornos logarítmicos; en imágenes, normalización o aumento de datos)."""