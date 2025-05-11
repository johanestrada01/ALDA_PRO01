# Script para la Generación de Datos Sintéticos de VIH en Colombia

## 1. Introducción

Este script de Python genera un conjunto de datos sintéticos que representan la evolución de diversos indicadores epidemiológicos y demográficos asociados al VIH en Colombia. Utiliza un conjunto base de datos reales para ciertos años y, a partir de estos, extrapola información para un rango de años definido por el usuario. El script incorpora tendencias predefinidas, fluctuaciones aleatorias y reglas de consistencia para asegurar la coherencia interna y plausibilidad epidemiológica de los datos generados. El resultado final incluye visualizaciones y un archivo CSV. 

## 2. Descripción del Código y Funcionamiento

El script se organiza en varias partes: definición de datos iniciales, funciones de generación y ajuste, el bucle principal de generación, y la visualización y exportación de resultados.

### 2.1. Librerías Utilizadas

El script utiliza las siguientes librerías de Python:

* **matplotlib.pyplot:** Para crear gráficos y visualizaciones. 
* **random:** Para introducir aleatoriedad en la generación de valores. 
* **math:** Para funciones matemáticas (ej., `math.exp` para la generación inicial de contagios). 
* **numpy:** Para operaciones numéricas, especialmente la creación de arrays para interpolación. 
* **pandas:** Para manipulación de datos como DataFrame y exportación a CSV. 
* **scipy.interpolate.make_interp_spline:** Para suavizar líneas en los gráficos. 

### 2.2. Estructuras de Datos Clave

* **`datos_reales` (Diccionario):** Almacena datos históricos de 2017 a 2024. Las claves son años, y los valores son listas de métricas. Los valores `None` indican datos no disponibles. 
* **`columnas` (Lista):** Define los nombres de las 29 variables (ej., "Contagios", "%Hombres", "%Sexual"). 
* **`anio_inicio` y `anio_fin` (Enteros):** Definen el rango de años para la generación de datos. Se solicitan al usuario, con valores por defecto 1981 y 2030. 
* **`grupos_complementarios` (Diccionario):** Establece relaciones entre porcentajes que deben sumar un total (usualmente 100%). Por ejemplo, `%Mujeres` = `100 - %Hombres`. 
* **`tendencias` (Diccionario):** Especifica parámetros para generar ciertas variables, incluyendo `tendencia` (cambio anual), `min` y `max`. 
* **`datos_gen` (Diccionario):** Almacena los datos generados. Las claves son nombres de columnas, y los valores son diccionarios anidados (año: valor). 

### 2.3. Funciones Principales

* **`obtener_promedio_historico(col)`:** Calcula el promedio de los valores en `datos_reales` para una columna. 
* **`obtener_tendencia_historica(col)`:** Calcula la pendiente promedio de los valores en `datos_reales` para una columna. 
* **`generar_contagios(año)`:** Genera el número de "Contagios".
    * Para años antes de `datos_reales` (antes de 2017): 
        * Si `año` < 1990: Crecimiento exponencial. 
        * Si 1990 <= `año` < 2000: Crecimiento exponencial con menor tasa. 
        * Si 2000 <= `año` < `min(datos_reales.keys())`: Valor anterior + tendencia creciente + fluctuación aleatoria. 
    * Para años después de `datos_reales` (después de 2024): 
        * Calcula la media de los últimos 4 años de `datos_reales`.
        * Aplica una variación anual aleatoria (-12% a +15%). 
        * Asegura un mínimo de 100 contagios. 
* **`ajustar_complementarias(principal, complementarias, año)`:** Asegura la consistencia entre variables en `grupos_complementarios`. 
    * Si hay una variable complementaria, calcula una a partir de la otra para sumar 100%.
    * Si hay múltiples variables, las ajusta proporcionalmente. 

### 2.4. Lógica de Generación de Datos

1.  Inicializa "Contagios" con los datos de `datos_reales`. 
2.  Genera "Contagios" para años fuera de `datos_reales` usando `generar_contagios(año)`. 
3.  Genera otras variables:
    * Para variables con tendencia definida (en `tendencias`): Usa el valor anterior (o promedio histórico o punto medio si no existe), agrega tendencia y ruido, y acota el valor.
    * Para otras variables: Usa el valor anterior + ruido gaussiano (o promedio histórico + ruido si no hay valor anterior), y acota entre 0 y 100 si es un porcentaje.
4.  Ajusta las variables complementarias con `ajustar_complementarias`.

### 2.5. Visualización y Exportación

* **Gráficos:** Genera gráficos de líneas para cada columna, mostrando datos reales y generados, e incluye una línea de promedio. 
* **Resumen en Consola:** Imprime una tabla con valores para años clave. 
* **Exportación a CSV:** Guarda los datos de `datos_gen` en `datos_vih.csv`. 

## 3. Similitud con la Realidad y Validación Epidemiológica

### 3.1. Fortalezas en la Aproximación a la Realidad

* **Base en Datos Reales:** Usa `datos_reales` (2017-2024) como punto de partida.
* **Modelado de Tendencias:** El diccionario `tendencias` simula comportamientos esperados (ej., aumento de la cobertura TAR, disminución de la letalidad). 
* **Simulación de Fases Epidémicas:** La función `generar_contagios` refleja las fases de una epidemia. 
* **Consistencia Interna:** `ajustar_complementarias` asegura la coherencia entre variables relacionadas. 
* **Introducción de Variabilidad:** El uso de `random` introduce variabilidad estocástica. 

### 3.2. Limitaciones y Naturaleza Pseudoaleatoria

* **No es un Modelo Predictivo Mecanicista:** No simula mecanismos de transmisión del VIH ni dinámicas poblacionales complejas. 
* **Simplificación de Interdependencias:** No modela interacciones complejas entre métricas. 
* **Dependencia de la Calidad de `datos_reales`:** La fiabilidad depende de la calidad de los datos reales. 
* **Fiabilidad de la Extrapolación a Largo Plazo:** La incertidumbre aumenta al alejarse de los años con datos reales. 
* **Naturaleza de la Aleatoriedad:** La forma del ruido es una simplificación. 
* **Valores Constantes o Poco Variables:** Algunos valores en `datos_reales` son constantes, lo que puede limitar la generación. 

## 4. Salida del Script

El script produce: 

1.  **Gráficos en Pantalla:** Ventanas de matplotlib con series temporales de variables. 
2.  **Tabla Resumen en Consola:** Vista tabular de indicadores clave para años seleccionados.
3.  **Archivo `datos_vih.csv`:** Contiene todos los datos generados en formato CSV. 

## 5. Conclusión

El script genera datos sintéticos sobre el VIH en Colombia, equilibrando la fidelidad a los datos históricos con la flexibilidad de generar series temporales extendidas. Es un generador de datos pseudoaleatorios, no un modelo epidemiológico predictivo. El archivo CSV es útil para análisis exploratorios o educativos, interpretado en el contexto de su metodología.
