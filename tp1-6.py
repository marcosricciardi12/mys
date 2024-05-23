import random
import matplotlib.pyplot as plt
import numpy as np
import os
import math


# os.environ["XDG_SESSION_TYPE"] = "wayland"
# os.environ["QT_QPA_PLATFORM"] = "wayland"

# # # TP 1-4

def temperatura_con_perdidas_calc(resistencia, temperatura_inicial_agua, temperatura_ambiente, voltaje_alimentacion):
    temperatura_con_perdidas = np.empty(0, dtype=float)
    temperatura_con_perdidas = np.append(temperatura_con_perdidas, temperatura_inicial_agua)
    potencia = voltaje_alimentacion**2/resistencia
    for index in range(1, len(x)):
        temperatura_con_perdidas  = np.append(temperatura_con_perdidas, temperatura_con_perdidas[index-1] + ((potencia - calor_perdido*(temperatura_con_perdidas[index-1]-temperatura_ambiente))/(1.2*4186)))
    return temperatura_con_perdidas

def temperatura_estocastico(resultado_ant, resistencia, temperatura_inicial_agua, temperatura_ambiente, voltaje_alimentacion):
    potencia = voltaje_alimentacion**2/resistencia
    temperatura_con_perdidas_elemento  = resultado_ant + ((potencia - calor_perdido*(resultado_ant-temperatura_ambiente))/(1.2*4186))
    return temperatura_con_perdidas_elemento


temperatura_inicial_agua = 8
temperatura_final_agua = 80
temperatura_ambiente = 15

tiempo_trabajo_incial = 0
tiempo_trabajo_final = 600 #600

delta_temperatura = temperatura_final_agua - temperatura_inicial_agua
voltaje_alimentacion = 12 #voltios
masa_agua = 1.2 #kg
calor_especifico_agua = 4186 #J/kg*ºC
cantidad_de_calor = masa_agua * calor_especifico_agua * delta_temperatura
potencia = cantidad_de_calor/tiempo_trabajo_final
#potencia = v²/R
resistencia = voltaje_alimentacion**2 / potencia
#
delta_temperatura_1s = potencia*1/(masa_agua*calor_especifico_agua)
print("Cantidad de Calor: ", cantidad_de_calor)
print("Potencia Calculada: ", potencia)
print("Resistencia Calucalada: ", resistencia)
print("Aumento de temperatura en un segundo (1S): ", delta_temperatura_1s)
input("Esperar:  ... ")

cct = 0.04 #Coeficiente de Conductividad termica
volumen_agua = 1.2
espesor_material = 0.0015
altura_recipiente = 0.2035
radio_recipiente = 0.0475
superficie_cilindro = 2*math.pi*altura_recipiente*radio_recipiente
superficie_tapa = math.pi*radio_recipiente**2
superficie_total = superficie_cilindro + superficie_tapa * 2
calor_perdido = cct * (superficie_total/espesor_material)

print("Superficie total: ", superficie_total)
print("Calor perdido: %f W/ºC" % (calor_perdido))
input("Esperar:  ... ")
tick_tiempo = 1

x = np.arange(tiempo_trabajo_incial,tiempo_trabajo_final, tick_tiempo)
temperatura_sin_perdidas = temperatura_inicial_agua + delta_temperatura_1s*x
print(x)
print(temperatura_sin_perdidas)
plt.plot(x,temperatura_sin_perdidas, label='Temperatura sin perdidas')
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')

plt.xlim([0, max(x)+max(x)*0.01])
plt.ylim([0, max(temperatura_sin_perdidas)+max(temperatura_sin_perdidas)*0.01])
temperatura_con_perdidas = np.empty(0, dtype=float)
temperatura_con_perdidas = np.append(temperatura_con_perdidas, 8.0)
temperatura_con_perdidas = temperatura_con_perdidas_calc(resistencia= resistencia, temperatura_ambiente=temperatura_ambiente, temperatura_inicial_agua=temperatura_inicial_agua, voltaje_alimentacion=voltaje_alimentacion)

plt.plot(x,temperatura_con_perdidas, label='Temperatura CON perdidas', marker='')
plt.legend()
plt.show()


###TP5

# # Distribución uniforme de 5 valores próximos de resistencias.

# resistencia_calculada = 0.24 #ohm
# cantidad_resistencias = 5
# variacion_porcentual = 0.05 #5%
# mitad_cant = cantidad_resistencias // 2
# x_list = [i - mitad_cant for i in range(cantidad_resistencias)]
# print(x_list)
# valores_resistencias = [round((resistencia_calculada + (variacion_porcentual * valor)), 3) for valor in x_list]
# print(valores_resistencias)

rango_minimo = resistencia - 0.1*resistencia
rango_maximo = resistencia + 0.1*resistencia

# Tomar 5 valores aleatorios dentro del rango
valores_resistencias = np.random.uniform(rango_minimo, rango_maximo, 5)
# valores_resistencias.sort()
print("Valores iniciales de Resistencias:", valores_resistencias)

for resistencia_uniforme in valores_resistencias:
    temperatura_con_perdidas = temperatura_con_perdidas_calc(resistencia= resistencia_uniforme, temperatura_ambiente=temperatura_ambiente, temperatura_inicial_agua=temperatura_inicial_agua, voltaje_alimentacion=voltaje_alimentacion)
    plt.plot(x,temperatura_con_perdidas, label=f'Resistencia = {str(round(resistencia_uniforme, 3))} Ohm', marker='')
    plt.legend()
plt.xlim([0, tiempo_trabajo_final])
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()



# # Distribución normal de 5 temperaturas iniciales del agua. Media 10, desvío standard=5

# Parámetros de la distribución normal
media = 10
desviacion_estandar = 5

# Generar valores aleatorios de una distribución normal
temperaturas_iniciales_agua = np.random.normal(media, desviacion_estandar, 1000)

# Tomar 5 valores aleatorios dentro del rango
temperaturas_iniciales_agua = np.random.choice(temperaturas_iniciales_agua, 5)
# temperaturas_iniciales_agua.sort()
print("Temperaturas iniciales del agua:", temperaturas_iniciales_agua)

for temperatura_inicial_agua_normal in temperaturas_iniciales_agua:
    temperatura_con_perdidas = temperatura_con_perdidas_calc(resistencia= resistencia, temperatura_ambiente=temperatura_ambiente, temperatura_inicial_agua=temperatura_inicial_agua_normal, voltaje_alimentacion=voltaje_alimentacion)
    plt.plot(x,temperatura_con_perdidas, label=f'Temp Inicial Agua = {str(round(temperatura_inicial_agua_normal, 3))}ºC', marker='')
    plt.legend()
plt.xlim([0, tiempo_trabajo_final])
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()

# # Distribución uniforme de 5 temperaturas iniciales del ambiente, entre -20 y 50 grados.

rango_minimo = -20
rango_maximo = 50

# Tomar 5 valores aleatorios dentro del rango
temperaturas_iniciales_ambiente = np.random.uniform(rango_minimo, rango_maximo, 5)
# temperaturas_iniciales_ambiente.sort()
print("Temperaturas iniciales del Ambiente:", temperaturas_iniciales_ambiente)

for temperatura_inicial_ambiente_uniforme in temperaturas_iniciales_ambiente:
    temperatura_con_perdidas = temperatura_con_perdidas_calc(resistencia= resistencia, temperatura_ambiente=temperatura_inicial_ambiente_uniforme, temperatura_inicial_agua=temperatura_inicial_agua, voltaje_alimentacion=voltaje_alimentacion)
    plt.plot(x,temperatura_con_perdidas, label=f'Temp inicial Ambiente = {str(round(temperatura_inicial_ambiente_uniforme, 3))}ºC', marker='')
    plt.legend()
plt.xlim([0, tiempo_trabajo_final])
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()

# # Distribución normal de 5 valores de tensión de alimentación Media 12 SD:4 o Media 220, SD 40.

# Parámetros de la distribución normal
media = 12
desviacion_estandar = 4

# Generar valores aleatorios de una distribución normal
valores_tension = np.random.normal(media, desviacion_estandar, 1000)

# Tomar 5 valores aleatorios dentro del rango
valores_tension = np.random.choice(valores_tension, 5)
# valores_tension.sort()
print("Valores iniciales de voltaje:", valores_tension)

for valor_tension_normal in valores_tension:
    temperatura_con_perdidas = temperatura_con_perdidas_calc(resistencia= resistencia, temperatura_ambiente=temperatura_ambiente, temperatura_inicial_agua=temperatura_inicial_agua, voltaje_alimentacion=valor_tension_normal)
    plt.plot(x,temperatura_con_perdidas, label=f'Voltaje = {str(round(valor_tension_normal, 3))} V', marker='')
    plt.legend()
plt.xlim([0, tiempo_trabajo_final])
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()

# # Simulaciones que contengan todas las familias de curvas previas.

for i in range(5):
    temperatura_con_perdidas = temperatura_con_perdidas_calc(
        resistencia= valores_resistencias[i], temperatura_ambiente=temperaturas_iniciales_ambiente[i], 
        temperatura_inicial_agua=temperaturas_iniciales_agua[i], 
        voltaje_alimentacion=valores_tension[i])
    print("\n\tSimulacion Nº%d:" % (i+1) + 
          "\n\t\tResistencia: %f Ohm" % (valores_resistencias[i]) + 
          "\n\t\tTemperatura inicial del agua: %fºC" % (temperaturas_iniciales_agua[i]) + 
          "\n\t\tTemperatura inicial del ambiente: %fºC" % (temperaturas_iniciales_ambiente[i]) +
          "\n\t\tVoltaje: %f" % (valores_tension[i]))
    
    plt.plot(x,temperatura_con_perdidas, label=f'Simulacion Nº {str(i+1)} V', marker='')
    plt.legend()

plt.xlim([0, tiempo_trabajo_final])
plt.ylim([0, 100])
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()


# # # TP6
temperatura_con_perdidas_estocastico = np.empty(0, dtype=float)
temperatura_con_perdidas_estocastico = np.append(temperatura_con_perdidas_estocastico, temperatura_inicial_agua)
probabilidad = 1 / 300
suceso = False
list_sucesos = []
list_sucesos_terminados = []
contador = 0
temperatura_ambiente_estocastico = temperatura_ambiente
print("\nTemperatura ambiente actual: %fºC" % temperatura_ambiente_estocastico)
for tick in range(tiempo_trabajo_incial, tiempo_trabajo_final-1, tick_tiempo):
    posible_suceso = np.random.random()
    if posible_suceso <= probabilidad and not suceso:
        suceso = True
        descenso_temperatura = random.randint(10, 50)
        temperatura_ambiente_estocastico -= descenso_temperatura
        tiempo = random.randint(50, 200)
        print("OCURRIO EL SUCESO!\nLa Temperaturá baja %fºC durante %d segundos" %(descenso_temperatura, tiempo))
        print("\tTemperatura ambiente actual: %fºC" % temperatura_ambiente_estocastico)
        list_sucesos.append(tick)
    if suceso:
        contador += 1
        if contador >= tiempo:
            suceso = False
            contador = 0
            temperatura_ambiente_estocastico = temperatura_ambiente
            list_sucesos_terminados.append(tick)
            print("El SUCESO TERMINO!!")
            print("\tTemperatura ambiente actual: %fºC" % temperatura_ambiente_estocastico)
    
    temperatura_con_perdidas_elemento = temperatura_estocastico(resultado_ant = temperatura_con_perdidas_estocastico[tick], resistencia= resistencia, temperatura_ambiente=temperatura_ambiente_estocastico, temperatura_inicial_agua=temperatura_inicial_agua, voltaje_alimentacion=voltaje_alimentacion)
    temperatura_con_perdidas_estocastico = np.append(temperatura_con_perdidas_estocastico, temperatura_con_perdidas_elemento)
for suceso_ocurrido in list_sucesos:
    plt.axvline(x=suceso_ocurrido, color='orange', linestyle='--', linewidth=1, label=f'Fenomeno Estocastico 1/300')
for suceso_terminado in list_sucesos_terminados:
    plt.axvline(x=suceso_terminado, color='purple', linestyle='--', linewidth=1, label=f'Fenomeno Estocastico terminado')
plt.plot(x,temperatura_con_perdidas_estocastico, label=f'Temperatura con perdidas', marker='')
plt.plot(x,temperatura_sin_perdidas, label='Temperatura sin perdidas')
plt.legend()
plt.xlim([0, tiempo_trabajo_final])
plt.grid(True)
plt.xlabel('Tiempo(Seg)')
plt.ylabel('Temperatura (ºC)')
plt.title('Temperatura/Tiempo')
plt.show()