# Script para la Generación de Datos Sintéticos de VIH en Colombia

## 1. Introducción

Este script de Python genera un conjunto de datos sintéticos que representan la evolución de diversos indicadores epidemiológicos y demográficos asociados al VIH en Colombia. Utiliza un conjunto base de datos reales para ciertos años y, a partir de estos, extrapola información para un rango de años definido por el usuario. El script incorpora tendencias predefinidas, fluctuaciones aleatorias y reglas de consistencia para asegurar la coherencia interna y plausibilidad epidemiológica de los datos generados. El resultado final incluye visualizaciones y un archivo CSV. [cite: 1, 2, 3, 4]

## 2. Descripción del Código y Funcionamiento

El script se organiza en varias partes: definición de datos iniciales, funciones de generación y ajuste, el bucle principal de generación, y la visualización y exportación de resultados. [cite: 5]

### 2.1. Librerías Utilizadas

El script utiliza las siguientes librerías de Python:

* **matplotlib.pyplot:** Para crear gráficos y visualizaciones. [cite: 6]
* **random:** Para introducir aleatoriedad en la generación de valores. [cite: 7]
* **math:** Para funciones matemáticas (ej., `math.exp` para la generación inicial de contagios). [cite: 8, 9]
* **numpy:** Para operaciones numéricas, especialmente la creación de arrays para interpolación. [cite: 9]
* **pandas:** Para manipulación de datos como DataFrame y exportación a CSV. [cite: 10]
* **scipy.interpolate.make_interp_spline:** Para suavizar líneas en los gráficos. [cite: 11]

### 2.2. Estructuras de Datos Clave

* **`datos_reales` (Diccionario):** Almacena datos históricos de 2017 a 2024. Las claves son años, y los valores son listas de métricas. Los valores `None` indican datos no disponibles. [cite: 12, 13, 14]
* **`columnas` (Lista):** Define los nombres de las 29 variables (ej., "Contagios", "%Hombres", "%Sexual"). [cite: 14, 15]
* **`anio_inicio` y `anio_fin` (Enteros):** Definen el rango de años para la generación de datos. Se solicitan al usuario, con valores por defecto 1981 y 2030. [cite: 16, 17]
* **`grupos_complementarios` (Diccionario):** Establece relaciones entre porcentajes que deben sumar un total (usualmente 100%). Por ejemplo, `%Mujeres` = `100 - %Hombres`. [cite: 18, 19]
* **`tendencias` (Diccionario):** Especifica parámetros para generar ciertas variables, incluyendo `tendencia` (cambio anual), `min` y `max`. [cite: 20, 21, 22]
* **`datos_gen` (Diccionario):** Almacena los datos generados. Las claves son nombres de columnas, y los valores son diccionarios anidados (año: valor). [cite: 23, 24]

### 2.3. Funciones Principales

* **`obtener_promedio_historico(col)`:** Calcula el promedio de los valores en `datos_reales` para una columna. [cite: 25, 26, 27]
* **`obtener_tendencia_historica(col)`:** Calcula la pendiente promedio de los valores en `datos_reales` para una columna. [cite: 27, 28]
* **`generar_contagios(año)`:** Genera el número de "Contagios". [cite: 29]
    * Para años antes de `datos_reales` (antes de 2017): [cite: 29]
        * Si `año` < 1990: Crecimiento exponencial. [cite: 29, 30]
        * Si 1990 <= `año` < 2000: Crecimiento exponencial con menor tasa. [cite: 30]
        * Si 2000 <= `año` < `min(datos_reales.keys())`: Valor anterior + tendencia creciente + fluctuación aleatoria. [cite: 30, 31]
    * Para años después de `datos_reales` (después de 2024): [cite: 31, 32, 33, 34, 35]
        * Calcula la media de los últimos 4 años de `datos_reales`. [cite: 32, 33, 34, 35]
        * Aplica una variación anual aleatoria (-12% a +15%). [cite: 32, 33, 34, 35]
        * Asegura un mínimo de 100 contagios. [cite: 35]
* **`ajustar_complementarias(principal, complementarias, año)`:** Asegura la consistencia entre variables en `grupos_complementarios`. [cite: 35, 36, 37, 38]
    * Si hay una variable complementaria, calcula una a partir de la otra para sumar 100%. [cite: 36, 37, 38]
    * Si hay múltiples variables, las ajusta proporcionalmente. [cite: 36, 37, 38]

### 2.4. Lógica de Generación de Datos

1.  Inicializa "Contagios" con los datos de `datos_reales`. [cite: 38, 39]
2.  Genera "Contagios" para años fuera de `datos_reales` usando `generar_contagios(año)`. [cite: 39]
3.  Genera otras variables: [cite: 40, 41, 42, 43, 44, 45]
    * Para variables con tendencia definida (en `tendencias`): Usa el valor anterior (o promedio histórico o punto medio si no existe), agrega tendencia y ruido, y acota el valor. [cite: 40, 41, 42, 43]
    * Para otras variables: Usa el valor anterior + ruido gaussiano (o promedio histórico + ruido si no hay valor anterior), y acota entre 0 y 100 si es un porcentaje. [cite: 43, 44, 45]
4.  Ajusta las variables complementarias con `ajustar_complementarias`. [cite: 45, 46]

### 2.5. Visualización y Exportación

* **Gráficos:** Genera gráficos de líneas para cada columna, mostrando datos reales y generados, e incluye una línea de promedio. [cite: 46, 47, 48]
* **Resumen en Consola:** Imprime una tabla con valores para años clave. [cite: 48, 49]
* **Exportación a CSV:** Guarda los datos de `datos_gen` en `datos_vih.csv`. [cite: 49]

## 3. Similitud con la Realidad y Validación Epidemiológica

### 3.1. Fortalezas en la Aproximación a la Realidad

* **Base en Datos Reales:** Usa `datos_reales` (2017-2024) como punto de partida. [cite: 50, 51, 52, 53, 54, 55]
* **Modelado de Tendencias:** El diccionario `tendencias` simula comportamientos esperados (ej., aumento de la cobertura TAR, disminución de la letalidad). [cite: 50, 51, 52, 53, 54, 55]
* **Simulación de Fases Epidémicas:** La función `generar_contagios` refleja las fases de una epidemia. [cite: 50, 51, 52, 53, 54, 55]
* **Consistencia Interna:** `ajustar_complementarias` asegura la coherencia entre variables relacionadas. [cite: 54]
* **Introducción de Variabilidad:** El uso de `random` introduce variabilidad estocástica. [cite: 55, 56, 57, 58, 59, 60, 61]

### 3.2. Limitaciones y Naturaleza Pseudoaleatoria

* **No es un Modelo Predictivo Mecanicista:** No simula mecanismos de transmisión del VIH ni dinámicas poblacionales complejas. [cite: 56, 57, 58, 59, 60, 61]
* **Simplificación de Interdependencias:** No modela interacciones complejas entre métricas. [cite: 59, 60, 61]
* **Dependencia de la Calidad de `datos_reales`:** La fiabilidad depende de la calidad de los datos reales. [cite: 61, 62, 63, 64, 65, 66, 67, 68]
* **Fiabilidad de la Extrapolación a Largo Plazo:** La incertidumbre aumenta al alejarse de los años con datos reales. [cite: 63, 64, 65, 66, 67, 68]
* **Naturaleza de la Aleatoriedad:** La forma del ruido es una simplificación. [cite: 63, 64, 65, 66, 67, 68]
* **Valores Constantes o Poco Variables:** Algunos valores en `datos_reales` son constantes, lo que puede limitar la generación. [cite: 66, 67, 68]

## 4. Salida del Script

El script produce: [cite: 68, 69, 70, 71, 72]

1.  **Gráficos en Pantalla:** Ventanas de matplotlib con series temporales de variables. [cite: 68, 69, 70, 71, 72]
2.  **Tabla Resumen en Consola:** Vista tabular de indicadores clave para años seleccionados. [cite: 68, 69, 70, 71, 72]
3.  **Archivo `datos_vih.csv`:** Contiene todos los datos generados en formato CSV. [cite: 71, 72, 73, 74, 75, 76, 77, 78]

## 5. Conclusión

El script genera datos sintéticos sobre el VIH en Colombia, equilibrando la fidelidad a los datos históricos con la flexibilidad de generar series temporales extendidas. Es un generador de datos pseudoaleatorios, no un modelo epidemiológico predictivo. El archivo CSV es útil para análisis exploratorios o educativos, interpretado en el contexto de su metodología. [cite: 73, 74, 75, 76, 77, 78]
