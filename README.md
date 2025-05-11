# Script para la Generación de Datos Sintéticos de VIH en Colombia

## 1. Introducción

Este script de Python genera un conjunto de datos sintéticos que representan la evolución de diversos indicadores epidemiológicos y demográficos asociados al VIH en Colombia[cite: 79, 80, 81, 82]. Utiliza un conjunto base de datos reales para ciertos años y, a partir de estos, extrapola información para un rango de años definido por el usuario[cite: 80]. El script incorpora tendencias predefinidas, fluctuaciones aleatorias y reglas de consistencia para asegurar la coherencia interna y plausibilidad epidemiológica de los datos generados[cite: 81]. El resultado final incluye visualizaciones y un archivo CSV[cite: 82].

## 2. Descripción del Código y Funcionamiento

El script se organiza en varias partes: definición de datos iniciales, funciones de generación y ajuste, el bucle principal de generación, y la visualización y exportación de resultados[cite: 83].

### 2.1. Librerías Utilizadas

El script utiliza las siguientes librerías de Python:

* **matplotlib.pyplot:** Para crear gráficos y visualizaciones[cite: 84].
* **random:** Para introducir aleatoriedad en la generación de valores[cite: 85].
* **math:** Para funciones matemáticas (ej., `math.exp` para la generación inicial de contagios)[cite: 86].
* **numpy:** Para operaciones numéricas, especialmente la creación de arrays para interpolación[cite: 87].
* **pandas:** Para manipulación de datos como DataFrame y exportación a CSV[cite: 88].
* **scipy.interpolate.make_interp_spline:** Para suavizar líneas en los gráficos[cite: 89].

### 2.2. Estructuras de Datos Clave

* **`datos_reales` (Diccionario):** Almacena datos históricos de 2017 a 2024. Las claves son años, y los valores son listas de métricas[cite: 90, 91]. Los valores `None` indican datos no disponibles.
* **`columnas` (Lista):** Define los nombres de las 29 variables (ej., "Contagios", "%Hombres", "%Sexual")[cite: 92, 93].
* **`anio_inicio` y `anio_fin` (Enteros):** Definen el rango de años para la generación de datos. Se solicitan al usuario, con valores por defecto 1981 y 2030[cite: 94, 95].
* **`grupos_complementarios` (Diccionario):** Establece relaciones entre porcentajes que deben sumar un total (usualmente 100%). Por ejemplo, `%Mujeres` = `100 - %Hombres`[cite: 96, 97].
* **`tendencias` (Diccionario):** Especifica parámetros para generar ciertas variables, incluyendo `tendencia` (cambio anual), `min` y `max`[cite: 98, 99, 100].
* **`datos_gen` (Diccionario):** Almacena los datos generados. Las claves son nombres de columnas, y los valores son diccionarios anidados (año: valor)[cite: 101, 102].

### 2.3. Funciones Principales

* **`obtener_promedio_historico(col)`:** Calcula el promedio de los valores en `datos_reales` para una columna[cite: 103, 104].
* **`obtener_tendencia_historica(col)`:** Calcula la pendiente promedio de los valores en `datos_reales` para una columna[cite: 105, 106].
* **`generar_contagios(año)`:** Genera el número de "Contagios"[cite: 107].
    * Para años antes de `datos_reales` (antes de 2017):
        * Si `año` < 1990: Crecimiento exponencial[cite: 107].
        * Si 1990 <= `año` < 2000: Crecimiento exponencial con menor tasa[cite: 108].
        * Si 2000 <= `año` < `min(datos_reales.keys())`: Valor anterior + tendencia creciente + fluctuación aleatoria[cite: 108, 109].
    * Para años después de `datos_reales` (después de 2024):
        * Calcula la media de los últimos 4 años de `datos_reales`[cite: 110, 111, 112].
        * Aplica una variación anual aleatoria (-12% a +15%)[cite: 111, 112].
        * Asegura un mínimo de 100 contagios[cite: 113].
* **`ajustar_complementarias(principal, complementarias, año)`:** Asegura la consistencia entre variables en `grupos_complementarios`[cite: 113, 114, 115].
    * Si hay una variable complementaria, calcula una a partir de la otra para sumar 100%[cite: 114].
    * Si hay múltiples variables, las ajusta proporcionalmente[cite: 115].

### 2.4. Lógica de Generación de Datos

1.  Inicializa "Contagios" con los datos de `datos_reales`[cite: 116, 117].
2.  Genera "Contagios" para años fuera de `datos_reales` usando `generar_contagios(año)`[cite: 117, 118].
3.  Genera otras variables:
    * Para variables con tendencia definida (en `tendencias`): Usa el valor anterior (o promedio histórico o punto medio si no existe), agrega tendencia y ruido, y acota el valor[cite: 118, 119, 120, 121].
    * Para otras variables: Usa el valor anterior + ruido gaussiano (o promedio histórico + ruido si no hay valor anterior), y acota entre 0 y 100 si es un porcentaje[cite: 121, 122, 123].
4.  Ajusta las variables complementarias con `ajustar_complementarias`[cite: 123, 124].

### 2.5. Visualización y Exportación

* **Gráficos:** Genera gráficos de líneas para cada columna, mostrando datos reales y generados, e incluye una línea de promedio[cite: 124, 125, 126].
* **Resumen en Consola:** Imprime una tabla con valores para años clave[cite: 126, 127].
* **Exportación a CSV:** Guarda los datos de `datos_gen` en `datos_vih.csv`[cite: 127, 128].

## 3. Similitud con la Realidad y Validación Epidemiológica

### 3.1. Fortalezas en la Aproximación a la Realidad

* **Base en Datos Reales:** Usa `datos_reales` (2017-2024) como punto de partida[cite: 128, 129].
* **Modelado de Tendencias:** El diccionario `tendencias` simula comportamientos esperados (ej., aumento de la cobertura TAR, disminución de la letalidad)[cite: 129, 130, 131].
* **Simulación de Fases Epidémicas:** La función `generar_contagios` refleja las fases de una epidemia[cite: 131, 132].
* **Consistencia Interna:** `ajustar_complementarias` asegura la coherencia entre variables relacionadas[cite: 132, 133].
* **Introducción de Variabilidad:** El uso de `random` introduce variabilidad estocástica[cite: 133, 134].

### 3.2. Limitaciones y Naturaleza Pseudoaleatoria

* **No es un Modelo Predictivo Mecanicista:** No simula mecanismos de transmisión del VIH ni dinámicas poblacionales complejas[cite: 134, 135, 136, 137].
* **Simplificación de Interdependencias:** No modela interacciones complejas entre métricas[cite: 137, 138, 139].
* **Dependencia de la Calidad de `datos_reales`:** La fiabilidad depende de la calidad de los datos reales[cite: 139, 140, 141].
* **Fiabilidad de la Extrapolación a Largo Plazo:** La incertidumbre aumenta al alejarse de los años con datos reales[cite: 141, 142, 143].
* **Naturaleza de la Aleatoriedad:** La forma del ruido es una simplificación[cite: 143, 144, 145, 146].
* **Valores Constantes o Poco Variables:** Algunos valores en `datos_reales` son constantes, lo que puede limitar la generación[cite: 143, 144, 145, 146].

## 4. Salida del Script

El script produce:

1.  **Gráficos en Pantalla:** Ventanas de matplotlib con series temporales de variables[cite: 146, 147, 148].
2.  **Tabla Resumen en Consola:** Vista tabular de indicadores clave para años seleccionados[cite: 148, 149, 150].
3.  **Archivo `datos_vih.csv`:** Contiene todos los datos generados en formato CSV[cite: 149, 150].

## 5. Conclusión

El script genera datos sintéticos sobre el VIH en Colombia, equilibrando la fidelidad a los datos históricos con la flexibilidad de generar series temporales extendidas[cite: 151, 152, 153, 154]. Es un generador de datos pseudoaleatorios, no un modelo epidemiológico predictivo[cite: 154, 155, 156]. El archivo CSV es útil para análisis exploratorios o educativos, interpretado en el contexto de su metodología[cite: 154, 155, 156].
