import matplotlib.pyplot as plt
import numpy as np
import os


# os.environ["XDG_SESSION_TYPE"] = "wayland"
# os.environ["QT_QPA_PLATFORM"] = "wayland"


temp_i = 8
temp_f = 80
delta_temp_total = temp_f - temp_i
delta_temp_1s = 0.12
tiempo_trabajo_incial = 0
tiempo_trabajo_final = 600 #600
calor_perdido = 1.997
tick_tiempo = 1
potencia = 602.7845

x = np.arange(tiempo_trabajo_incial,tiempo_trabajo_final, tick_tiempo)
y = temp_i + delta_temp_1s*x
print(x)
print(y)
plt.plot(x,y, label='Temperatura sin perdidas')
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')

plt.xlim([0, max(x)+max(x)*0.01])
plt.ylim([0, max(y)+max(y)*0.01])
# no 10002 si no 602.7845
y1 = np.empty(0, dtype=float)
y1 = np.append(y1, 8.0)
for index in range(1, len(x)):
     y1  = np.append(y1, y1[index-1] + ((potencia - calor_perdido*y1[index-1])/(1.2*4186)))
     # print(y1[index])

plt.plot(x,y1, label='Temperatura CON perdidas', marker='')
plt.legend()
plt.show()