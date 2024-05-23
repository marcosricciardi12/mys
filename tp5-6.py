import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import os


# # os.environ["XDG_SESSION_TYPE"] = "wayland"
# # os.environ["QT_QPA_PLATFORM"] = "wayland"


# temp_i = 8
# temp_f = 80
# delta_temp_total = temp_f - temp_i
# delta_temp_1s = 0.12
# tiempo_trabajo_incial = 0
# tiempo_trabajo_final = 600 #600
# calor_perdido = 1.997
# tick_tiempo = 1
# potencia = 602.7845

# x = np.arange(tiempo_trabajo_incial,tiempo_trabajo_final, tick_tiempo)
# y = temp_i + delta_temp_1s*x
# print(x)
# print(y)
# plt.plot(x,y, label='Temperatura sin perdidas')
# plt.grid(True)
# plt.xlabel('Tiempo(Seg)')
# plt.ylabel('Temperatura (ºC)')
# plt.title('Temperatura/Tiempo')

# plt.xlim([0, max(x)+max(x)*0.01])
# plt.ylim([0, max(y)+max(y)*0.01])
# # no 10002 si no 602.7845
# y1 = np.empty(0, dtype=float)
# y1 = np.append(y1, 8.0)
# for index in range(1, len(x)):
#      y1  = np.append(y1, y1[index-1] + ((potencia - calor_perdido*y1[index-1])/(1.2*4186)))
#      # print(y1[index])

# plt.plot(x,y1, label='Temperatura CON perdidas', marker='')
# plt.legend()
# plt.show()


# Distribución uniforme de 5 valores próximos de resistencias.

resistencia_calculada = 0.24 #ohm
cantidad_resistencias = 5
variacion_porcentual = 0.05 #5%
mitad_cant = cantidad_resistencias // 2
x_list = [i - mitad_cant for i in range(cantidad_resistencias)]
print(x_list)
valores_resistencias = [round((resistencia_calculada + (variacion_porcentual * valor)), 3) for valor in x_list]
print(valores_resistencias)


# Parámetros de la distribución uniforme
low = min(valores_resistencias)  # Límite inferior
high = max(valores_resistencias)  # Límite superior
size = 1000 # Número de muestras

# Generar datos
data = np.random.uniform(low, high, size)

# Crear el histograma
plt.hist(data, bins=cantidad_resistencias, density=True, alpha=0.6, color='g', edgecolor='black')

# Añadir etiquetas y título
plt.xlabel('Valores de resistencias')
plt.ylabel('Densidad de probabilidad')
plt.title('Histograma Distribución Uniforme para 5 valores de resistencias')

# Mostrar el gráfico
plt.show()

# Distribución normal de 5 temperaturas iniciales del agua. Media 10, desvío standard=5

import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la distribución normal
media = 10
desviacion_estandar = 5

# Generar 1000 valores de temperaturas iniciales
temperaturas_iniciales = np.random.normal(media, desviacion_estandar, 1000)

# Crear el histograma de las temperaturas iniciales
plt.hist(temperaturas_iniciales, bins=5, edgecolor='black', density=True, alpha=0.7)

# Añadir línea vertical para la media
plt.axvline(x=media, color='orange', linestyle='--', label='Media')

# Añadir etiquetas y título
plt.xlabel('Temperatura')
plt.ylabel('Densidad de Probabilidad')
plt.title('Histograma de Temperaturas Iniciales')

# Añadir leyenda
plt.legend()

# Mostrar el gráfico
plt.show()

# Distribución uniforme de 8 temperaturas iniciales del ambiente, entre -20 y 50 grados.


# Distribución normal de 5 valores de tensión de alimentación Media 12 SD:4 o Media 220, SD 40.


# Simulaciones que contengan todas las familias de curvas previas.
