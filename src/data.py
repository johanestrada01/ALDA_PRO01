import matplotlib.pyplot as plt
import random
import math
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

datos_reales = {
    2017: [13311, 80.0, 20.0, 61.0, 39.0, 99.0, 1.0, 56.3, 36.7, 6.0, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, None, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2018: [14747, 80.0, 20.0, 61.0, 39.0, 99.0, 1.0, 53.1, 39.3, 6.6, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, None, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2019: [17346, 80.7, 19.3, 61.5, 38.5, 98.5, 1.5, 51.3, 40.7, 6.5, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, None, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2020: [13605, 80.0, 20.0, 61.0, 39.0, 92.47, 7.53, 56.4, 36.8, 6.1, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, 20.4, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2021: [9210, 77.4, 22.6, 61.0, 39.0, 98.5, 1.5, 53.2, 39.4, 6.4, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, None, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2022: [17271, 80.8, 19.2, 62.0, 38.0, 98.5, 1.5, 51.4, 40.8, 6.3, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, 36.3, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2023: [20540, 80.5, 19.5, 62.0, 38.0, 98.5, 1.5, 56.5, 36.9, 6.2, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, 39.3, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
    2024: [17902, 80.7, 19.3, 62.1, 37.9, 98.5, 1.5, 53.3, 39.5, 6.2, 0.5, 0.36, 0.1, 39.0, 61.0, 95.0, 72.7, 68.35, 95.3, 0.49, None, 270, 0.5, 1.6, 1.5, 2.8, 10.0, 90.0, 3.5],
}

columnas = [
    "Contagios", "%Hombres", "%Mujeres", "%Menores34", "%Mayores34", "%Sexual", "%NoSexual",
    "%Hetero", "%Homo", "%Bi", "%Perinatal", "%Drogas intectables", "%Transfusion", "%Diagnostico Tardio", "%Diagnostico Temprano",
    "%Tratamiento antirretroviral", "%Supresión≤1000", "%Supresión≤50", "%Gestantes Tratamiento", "%Transmisión Vertical", "Incidencia/100k", "Prevalencia/100k",
    "T/Mortal/100k", "Letalidad", "%Indígenas", "%Afro", "%Rural", "%Urbano", "Ratio H/M"
]

anio_inicio = input("Año de inicio (default 1981): ")
anio_inicio = int(anio_inicio) if anio_inicio and anio_inicio.isdigit() else 1981
anio_fin = input("Año de fin (default 2030): ")
anio_fin = int(anio_fin) if anio_fin and anio_fin.isdigit() else 2030

grupos_complementarios = {
    "%Hombres": ["%Mujeres"],
    "%Menores34": ["%Mayores34"],
    "%Sexual": ["%NoSexual"],
    "%Hetero": ["%Homo", "%Bi"],
    "%Diagnostico Tardio": ["%Diagnostico Temprano"],
    "%Rural": ["%Urbano"]
}

tendencias = {
    "%Hombres": {"tendencia": 0.1, "min": 75, "max": 82},
    "%Menores34": {"tendencia": 0.05, "min": 58, "max": 65},
    "%Sexual": {"tendencia": 0.1, "min": 90, "max": 99.5},
    "%Hetero": {"tendencia": -0.1, "min": 45, "max": 60},
    "%Homo": {"tendencia": 0.08, "min": 35, "max": 45},
    "%Bi": {"tendencia": 0.02, "min": 5, "max": 10},
    "%Tratamiento antirretroviral": {"tendencia": 0.2, "min": 90, "max": 98},
    "%Supresión≤1000": {"tendencia": 0.1, "min": 70, "max": 85},
    "%Supresión≤50": {"tendencia": 0.2, "min": 65, "max": 80},
    "%Gestantes Tratamiento": {"tendencia": 0.05, "min": 90, "max": 99},
    "%Transmisión Vertical": {"tendencia": -0.01, "min": 0.1, "max": 0.8},
    "Letalidad": {"tendencia": -0.05, "min": 0.5, "max": 2.5}
}

datos_gen = {col: {} for col in columnas}

def obtener_promedio_historico(col):
    valores = [datos_reales[año][idx] for año, datos in datos_reales.items() 
               for idx, c in enumerate(columnas) if c == col and datos[idx] is not None]
    return sum(valores) / len(valores) if valores else None

def obtener_tendencia_historica(col):
    valores = [(año, datos_reales[año][idx]) for año, datos in datos_reales.items() 
               for idx, c in enumerate(columnas) if c == col and datos[idx] is not None]
    if len(valores) < 2:
        return 0
    
    pendientes = [(valores[i][1] - valores[i-1][1]) / (valores[i][0] - valores[i-1][0]) 
                 for i in range(1, len(valores))]
    return sum(pendientes) / len(pendientes) if pendientes else 0

def generar_contagios(año):
    if año < min(datos_reales.keys()):
        if año < 1990:
            return int(50 * math.exp((año - 1981) * 0.2))
        elif año < 2000:
            return int(500 * math.exp((año - 1990) * 0.15))
        else:
            año_anterior = año - 1
            valor_anterior = datos_gen["Contagios"].get(año_anterior, 5000)
            tendencia = 200 + (año - 2000) * 50
            fluctuacion = random.uniform(-0.15, 0.15) * valor_anterior
            return max(100, int(valor_anterior + tendencia + fluctuacion))
    
    if año > max(datos_reales.keys()):
        años_recientes = sorted([a for a in datos_reales.keys()])[-4:]
        valores_recientes = [datos_reales[a][0] for a in años_recientes]
        
        media = sum(valores_recientes) / len(valores_recientes)
        
        variacion_anual = random.uniform(-0.12, 0.15)
        incremento = variacion_anual * media
        
        año_anterior = año - 1
        base = datos_gen["Contagios"].get(año_anterior, media)
        
        return max(100, int(base + incremento))

def ajustar_complementarias(principal, complementarias, año):
    if principal not in datos_gen or año not in datos_gen[principal]:
        return
    
    valor_principal = datos_gen[principal][año]
    if valor_principal is None:
        return
    
    if len(complementarias) == 1 and "%" in principal and "%" in complementarias[0]:
        compl = complementarias[0]
        if compl in datos_gen:
            datos_gen[compl][año] = round(100 - valor_principal, 2)
    
    elif len(complementarias) > 1 and all("%" in c for c in [principal] + complementarias):
        valores_comp = {}
        suma_comp = 0
        for comp in complementarias:
            if comp in datos_gen and año in datos_gen[comp] and datos_gen[comp][año] is not None:
                valores_comp[comp] = datos_gen[comp][año]
                suma_comp += valores_comp[comp]
            else:
                prom = obtener_promedio_historico(comp)
                if prom is not None:
                    valores_comp[comp] = prom
                    suma_comp += prom
                else:
                    valores_comp[comp] = 100 - valor_principal / len(complementarias)
                    suma_comp += valores_comp[comp]
        
        objetivo = 100 - valor_principal
        
        if suma_comp > 0:
            factor = objetivo / suma_comp
            for comp in complementarias:
                if comp in valores_comp:
                    datos_gen[comp][año] = round(valores_comp[comp] * factor, 2)

for año in datos_reales:
    datos_gen["Contagios"][año] = datos_reales[año][0]
for año in range(anio_inicio, anio_fin + 1):
    if año not in datos_reales and "Contagios" not in datos_gen.get(año, {}):
        datos_gen["Contagios"][año] = generar_contagios(año)

    for col in columnas[1:]: 
        if col in tendencias:
            config = tendencias[col] 
            año_anterior = año - 1
            if año_anterior in datos_gen[col] and datos_gen[col][año_anterior] is not None:
                base = datos_gen[col][año_anterior]
            else:
                base = obtener_promedio_historico(col)
                if base is None:
                    base = (config["min"] + config["max"]) / 2
            tendencia_anual = random.choice([x for x in range(-8, 8)]) * config["tendencia"] + random.uniform(-0.5, 0.5)
            nuevo_valor = base + tendencia_anual
            nuevo_valor = max(config["min"], min(config["max"], nuevo_valor))
            datos_gen[col][año] = round(nuevo_valor, 2)
        
        elif col not in ["%Mujeres", "%Mayores34", "%NoSexual"]:
            # Valor del año anterior, si existe:
            if año - 1 in datos_gen[col] and datos_gen[col][año-1] is not None:
                prev = datos_gen[col][año-1]
                # ruido: 2% del valor anterior, distrib. normal
                sigma = max(abs(prev) * 0.02, 0.005)
                ruido = random.gauss(0, sigma)
                nuevo_valor = prev + ruido
            else:
                # Si no hay 'previo', usar promedio histórico con ruido inicial
                prom = obtener_promedio_historico(col)
                if prom is not None:
                    sigma = max(prom * 0.02, 0.005)
                    ruido = random.gauss(0, sigma)
                    nuevo_valor = prom + ruido
                else:
                    nuevo_valor = None

            if nuevo_valor is not None:
                if "%" in col:
                    # Acotar a [0,100]
                    nuevo_valor = max(0, min(100, nuevo_valor))
                # Guardar con suficiente precisión si es muy pequeño
                datos_gen[col][año] = round(nuevo_valor, 4 if "%" in col and nuevo_valor < 1 else 2)

for año in range(anio_inicio, anio_fin + 1):
    for principal, complementarias in grupos_complementarios.items():
        ajustar_complementarias(principal, complementarias, año)

# for col in columnas:
#     años = sorted(año for año in range(anio_inicio, anio_fin + 1) if año in datos_gen[col] and datos_gen[col][año] is not None)
#     if not años:
#         continue
        
#     vals = [datos_gen[col][a] for a in años]
    
#     plt.figure(figsize=(10, 4))
    
#     años_reales = [a for a in años if a in datos_reales]
#     años_gen = [a for a in años if a not in datos_reales]
#     vals_reales = [datos_gen[col][a] for a in años_reales]
#     vals_gen = [datos_gen[col][a] for a in años_gen]
    
#     if len(años) > 3:
#         años_array = np.array(años)
#         vals_array = np.array(vals)
        
#         if len(años) > 5:
#             try:
#                 spl = make_interp_spline(años_array, vals_array, k=min(3, len(años)-1))
#                 años_suaves = np.linspace(min(años), max(años), 300)
#                 vals_suaves = spl(años_suaves)
#                 plt.plot(años_suaves, vals_suaves, '-', color='blue', alpha=0.5)
#             except:
#                 plt.plot(años, vals, '-', color='blue', alpha=0.5)
#         else:
#             plt.plot(años, vals, '-', color='blue', alpha=0.5)
    
#     if años_reales:
#         plt.plot(años_reales, vals_reales, 'o', color='green', label='Datos reales' if col == "Contagios" else 'Años con datos reales')
    
#     if años_gen:
#         plt.plot(años_gen, vals_gen, 'o', color='orange', markersize=4, alpha=0.7, label='Datos generados')
    
#     nums = [v for v in vals if isinstance(v, (int, float))]
#     if nums:
#         prom = sum(nums) / len(nums)
#         plt.axhline(prom, color='r', linestyle='--', alpha=0.5, label=f'Promedio: {round(prom, 2)}')
    
#     plt.title(col)
#     plt.xlabel("Año")
#     plt.ylabel(col)
#     plt.grid(True, alpha=0.3)
#     plt.legend()
    
#     if "%" in col:
#         y_min = max(0, min(nums) * 0.9) if nums else 0
#         y_max = min(100, max(nums) * 1.1) if nums else 100
#         plt.ylim(y_min, y_max)
    
#     plt.tight_layout()
#     plt.show()

años_muestra = sorted([año for año in range(anio_inicio, anio_fin+1, 5)] + list(datos_reales.keys()))
años_muestra = sorted(set([a for a in años_muestra if anio_inicio <= a <= anio_fin]))

# print("\nResumen de datos para años clave:")
# print("-" * 80)
# print(f"{'Año':<8}", end="")
# for col in ["Contagios", "%Hombres", "%Sexual", "%Hetero", "%Homo", "%Bi", "Letalidad"]:
#     print(f"{col:<12}", end="")
# print()
# print("-" * 80)

# for año in años_muestra:
#     print(f"{año:<8}", end="")
#     for col in ["Contagios", "%Hombres", "%Sexual", "%Hetero", "%Homo", "%Bi", "Letalidad"]:
#         val = datos_gen[col].get(año)
#         if val is None:
#             print(f"{'N/A':<12}", end="")
#         elif isinstance(val, int):
#             print(f"{val:<12}", end="")
#         else:
#             print(f"{val:.2f}{'%' if '%' in col else '':<12}", end="")
#     print()


df = pd.DataFrame(datos_gen)


df = df.reindex(range(anio_inicio, anio_fin + 1))


df.index.name = 'Año'


df.to_csv('datos_vih.csv', encoding='utf-8')
print("Datos exportados correctamente a datos_vih.csv")