import matplotlib.pyplot as plt
import numpy as np
import os


os.environ["XDG_SESSION_TYPE"] = "wayland"
os.environ["QT_QPA_PLATFORM"] = "wayland"


temp_i = 8
temp_f = 80
delta_temp_total = temp_f - temp_i
delta_temp_1s = 0.12
tiempo_trabajo_incial = 0
tiempo_trabajo_final = 600
calor_perdido = 9.21
tick_tiempo = 1

x = np.arange(tiempo_trabajo_incial,tiempo_trabajo_final, tick_tiempo)
y = delta_temp_total + delta_temp_1s*x
plt.plot(x,y)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()
