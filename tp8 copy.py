# # Introducción.
# # Estamos presenciando un aumento de la competencia entre los diversos prestadores de servicios, que intentan captar más clientes y lograr mayor participación de mercado, manteniendo los clientes actuales, sin perderlos, con los perjuicios que ello ocasiona.

# # Por ello, este modelo tiende a demostrar cuál es la mejor alternativa de habilitación de boxes de atención, para lograr mayor cantidad de personas atendidas, en el menor tiempo posible.

# # El modelo es aplicable a cajas de supermercados, a bancos, locales de comida y, en general, en todos los centros de prestación en donde los clientes se ubican en colas que pueden derivar en pérdidas importante de tiempo. Como se dice habitualmente "time is money". Muchas veces las empresas pierden de vista el valor estratégico de la pronta y correcta atención de los clientes.
# # Un mal diseño de este servicio puede derivar en la pérdida de operaciones y en la lisa y llana pérdida del cliente, con todas las operaciones potenciales que no se realizarán nunca con estas personas.

# # Descripción.
# # Se trata de un local de servicios que puede contar con 1 a 10 boxes de atención de clientes,.
# # Al momento de iniciar la simulación se elige este parámetro.
# # Luego, la simulación responde a las siguientes reglas e hipótesis:
# # 1) El local abre de 8 a 12 horas.
# # 2) El cliente que ingresa es atendido en la zona de atención o pasa a una cola.
# # 3) Los clientes que están en cola o siendo atendidos pueden permanecer luego de la hora de cierre.
# # 4) Los clientes que no están siendo atendidos abandonarán el local a los 30 minutos.
# # 5) En cada segundo que transcurre, desde la apertura del local, la probabilidad de que ingrese un cliente es p=1/144.
# # 6) La cantidad de boxes activos se establece antes de correr la simulación.
# # 7) El tiempo de atención en cada box responde a una distribución normal, con media=10 minutos y desvio estándar=5 minutos.
# # 8) Mantener el box abierto durante toda la mañana cuesta $1000.
# # 9) Cada cliente que se va sin ser atendido representa una pérdida de $10.000.
# # 10) Todo dato requerido para diseñar y programar la simulación puede ser asumido o especificado adicionalmente por cada uno de Ustedes.

# # Resultados.
# # Al final de cada simulación, deberemos responder a los siguientes interrogantes:
# # 1) Cuántos clientes ingresaron al local?
# # 2) Cuántos clientes fueron atendidos?
# # 3) Cuántos clientes no fueron atendidos? Es decir abandonaron el local por demoras.
# # 4) Tiempo mínimo de atención en box.
# # 5) Tiempo máximo de atención en box.
# # 6) Tiempo mínimo de espera en salón.
# # 7) Tiempo máximo de espera en salón.
# # 8) Costo de la operación: costo del box+costo por pérdida de clientes.
# # 9) Presentación gráfica animada de cada proceso simulado, con diversas velocidades. Archivo AVI.

import datetime
import math
import random
import numpy as np
import csv
import matplotlib.pyplot as plt


import numpy as np

import scipy.stats as stats

def calcular_probabilidad_normal(media, desviacion_estandar, a, b):
    # Calcular la CDF en los puntos a y b
    cdf_a = stats.norm.cdf(a, loc=media, scale=desviacion_estandar)
    cdf_b = stats.norm.cdf(b, loc=media, scale=desviacion_estandar)
    
    # La probabilidad de que X esté entre a y b es la diferencia entre las CDFs
    probabilidad = cdf_b - cdf_a
    
    return probabilidad

def generar_numero_normal_limitedo_entero_unico(media, desviacion_estandar, limite_inferior, limite_superior):
    numeros_generados = set()
    while True:
        numero = random.normalvariate(media, desviacion_estandar)
        numero_entero = round(numero)  # Convertir el número a entero
        if limite_inferior <= numero_entero <= limite_superior and numero_entero not in numeros_generados:
            numeros_generados.add(numero_entero)
            return numero_entero
    
        
def generar_clientes(tiempo_trabajo, probabilidad):
    clientes = 0
    media = 7200
    desviacion_estandar = 7200
# Simulación del tiempo_trabajo
    suceso_instante = []
    for i in range(int(tiempo_trabajo/2)):
        if random.random() < 0.05*calcular_probabilidad_normal(media, desviacion_estandar,0, i):
            clientes += 1
            suceso_instante.append(True)
        else:
            suceso_instante.append(False)
    for i in range(int(tiempo_trabajo/2)):
        if random.random() < 0.05*calcular_probabilidad_normal(media, desviacion_estandar,int(tiempo_trabajo/2), int(tiempo_trabajo) - i):
            clientes += 1
            suceso_instante.append(True)
        else:
            suceso_instante.append(False)

    conteos = []
    intervalo = 1800
    for i in range(0, len(suceso_instante), intervalo):
        conteo = suceso_instante[i:i+intervalo].count(True)
        conteos.append(conteo)

    plt.bar(range(len(conteos)), conteos, width=0.8, edgecolor='black', alpha=0.7)
    # print(f"El número aleatorio generado dentro del intervalo es: {numero_aleatorio}")
    plt.xlabel('Intervalo de tiempo (cada 3600 segundos)')
    plt.ylabel('Número de eventos (True)')
    plt.title('Número de eventos True por intervalo de tiempo')
    plt.xticks(range(len(conteos)), [f'{i*intervalo}-{(i+1)*intervalo}' for i in range(len(conteos))], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return suceso_instante
    
def validar_horario_convertir(horario):
    try:
        hora_min  = horario.split(":")
        hora = int(hora_min[0])
        minutos = int(hora_min[1])
        horario_date = datetime.time(0, 0, 0)
        if (hora >= 0 and hora <= 23 and minutos >= 0  and minutos <= 59):
            segundos = 0
            horario_date = datetime.time(hora, minutos, segundos)
            return True, horario_date
        else:
            False, horario_date
    except:
        return False, horario_date

def setear_horario():
    while True:
        try:
            input_hora = input("Ingrese hora (Formato de 24hrs tipo HH:MM): ")
            hora_valida, horario_date = validar_horario_convertir(input_hora)
            if  not hora_valida:
                raise ValidarHoraError("Formato de hora inválido")
            else:
                fecha_sistema = datetime.datetime.now().date()
                horario_date = datetime.datetime.combine(fecha_sistema, horario_date)
                return horario_date
        except:
            print("Formato de hora inválido, intente nuevamente")

def suceso_cliente_ingresa(probabilidad):
    # Generar un número aleatorio entre 0 y 1
    numero_aleatorio = random.random()
    # Verificar si el número cae dentro del rango de la probabilidad
    return numero_aleatorio < probabilidad

class ValidarHoraError(Exception):
    pass

class ValidarBoxesError(Exception):
    pass

class Cliente():
    def __init__(self, instante_de_ingreso_al_local) -> None:
        self.siendo_atendido = False
        self.fue_atendido = False
        self.instante_ingreso_local = instante_de_ingreso_al_local
        self.instante_comienzo_atencion_box = None
        self.instante_fin_atencion = None
        self.tiempo_atencion = None
        self.tiempo_espera_max = 30*60
        self.tiempo_esperado = None


    def set_cliente_siendo_atendido(self, instante_inicio_atencion):
        self.siendo_atendido = True
        self.instante_comienzo_atencion_box = instante_inicio_atencion
        self.tiempo_esperado = self.instante_comienzo_atencion_box - self.instante_ingreso_local
        tiempo_atencion = int((np.random.normal(10, 5)) * 60)
        if tiempo_atencion < 60:
            self.tiempo_atencion = 60
        else:
            self.tiempo_atencion = tiempo_atencion

    def set_cliente_fue_atendido(self):
        self.siendo_atendido = False
        self.fue_atendido = True

    def terminar_atencion(self, tiempo_instante_actual):
        if  tiempo_instante_actual - self.instante_comienzo_atencion_box >= self.tiempo_atencion:
            self.set_cliente_fue_atendido()
            return True
        else:
            return False

    def cliente_seguir_esperando(self, instante_actual):
        if instante_actual-self.instante_ingreso_local >= self.tiempo_espera_max:
            self.tiempo_esperado = self.tiempo_espera_max
            return False
        else:
            return True
        
    



class Box():
    def __init__(self, box_numero) -> None:
        self.status = True
        self.cliente = None
        self.box_numero = box_numero

    def free_box(self):
        self.status = True
        self.cliente = None
    
    def lock_box(self, cliente):
        self.status = False
        self.cliente = cliente



class Local():
    def __init__(self) -> None:
        self.cantidad_boxes = self.set_cant_boxes()
        self.boxes = [Box(i) for i in range(int(self.cantidad_boxes))]
        self.hora_apertura = None
        self.hora_cierre = None
        self.tiempo_trabajo = None
        self.cola = []
        self.clientes_fueron_atendidos = []
        self.clientes_no_fueron_atendidos = []
        self.clientes = []
        self.probabilidad_cliente = 1/144
        self.costo_box = 1000
        self.costo_cliente_perdido = 10000
        self.perfida_total = None
        self.tiempo_maximo_atencion = None
        self.tiempo_minimo_atencion = None
        self.tiempo_minimo_espera = None
        self.tiempo_maximo_espera = None

    def calcular_perdida_total (self):
        self.perfida_total = self.costo_box * self.cantidad_boxes + self.costo_cliente_perdido * len(self.clientes_no_fueron_atendidos)
        return self.perfida_total
    
    def calcular_tiempo_max_min(self):
        max_espera_value = self.clientes_fueron_atendidos[0].tiempo_esperado
        min_espera_value = self.clientes_fueron_atendidos[0].tiempo_esperado
        max_atencion_value = self.clientes_fueron_atendidos[0].tiempo_atencion
        min_atencion_value = self.clientes_fueron_atendidos[0].tiempo_atencion
        for cliente in self.clientes_fueron_atendidos:
            if cliente.tiempo_esperado > max_espera_value:
                max_espera_value = cliente.tiempo_esperado
            if cliente.tiempo_esperado < min_espera_value:
                min_espera_value = cliente.tiempo_esperado
       
            if cliente.tiempo_atencion > max_atencion_value:
                max_atencion_value = cliente.tiempo_atencion
            if cliente.tiempo_atencion < min_atencion_value:
                min_atencion_value = cliente.tiempo_atencion

            if cliente.tiempo_atencion < 0 :
                print(cliente.__dict__.items())
        
        self.tiempo_maximo_atencion = max_atencion_value
        self.tiempo_minimo_atencion = min_atencion_value
        self.tiempo_minimo_espera = min_espera_value
        self.tiempo_maximo_espera = max_espera_value

    def set_cant_boxes(self):
        while True:
            try:
                input_boxes = int(input("Ingrese la cantidad de boxes: "))
                if  (input_boxes <= 0 or input_boxes > 10):
                    raise ValidarHoraError("Cantidad invalida, debe ser mayor a 0 y menor o igual que 10")
                else:
                    return input_boxes
            except:
                print("Cantidad de boxes invalida, debe ser mayor a 0 y menor o igual que 10")

    def set_parametros(self):
        print("Definir hora de apertura: ")
        self.hora_apertura = setear_horario()
        print("Definir hora de cierre: ")
        self.hora_cierre = setear_horario()
        print("\n\tHora de apertura: ", self.hora_apertura)
        print("\n\tHora de cierre: ", self.hora_cierre)

    def set_tiempo_trabajo(self):
        diferencia = self.hora_cierre - self.hora_apertura
        self.tiempo_trabajo = int(diferencia.total_seconds())
        print("\nTiempo de trabajo en segundos: ", self.tiempo_trabajo)
        
    def ingreso_cliente(self, instante_de_ingreso_al_local):
        cliente = Cliente(instante_de_ingreso_al_local)
        self.clientes.append(cliente)
        for box in self.boxes:
            if box.status:
                box.lock_box(cliente)
                cliente.set_cliente_siendo_atendido(instante_de_ingreso_al_local)
                print("Ingreso un cliente directo al box")
                return
        if not cliente.siendo_atendido:
            self.cola.insert(0, cliente)
            print("Ingreso un cliente a la cola de espera")

    def simulacion(self):
        lista_instante_sucesos = generar_clientes(self.tiempo_trabajo, self.probabilidad_cliente)
        archivo_instante = open("resultado_instante.csv", mode='w', newline='')
        escritor_csv = csv.writer(archivo_instante)
        escritor_csv.writerow(['Instante de tiempo', 'Total de clientes que ingresaron', "Clientes en cola de espera", 'Clientes siendo atendidos',
                                   "Clientes ya atendidos", "Clientes NO atendidos",
                                   ])
        

        clientes_siendo_atendidos = 0
        instante_tiempo = -1
        while len(self.cola) != 0 or clientes_siendo_atendidos != 0 or instante_tiempo <= self.tiempo_trabajo:
            instante_tiempo += 1 
            clientes_siendo_atendidos = 0

            if instante_tiempo < self.tiempo_trabajo:
                if lista_instante_sucesos[instante_tiempo]:
                    print(instante_tiempo)
                    self.ingreso_cliente(instante_tiempo)
                
            
            for box in self.boxes:
                if box.cliente is not None:
                    clientes_siendo_atendidos += 1
                    if box.cliente.terminar_atencion(instante_tiempo):
                        if clientes_siendo_atendidos > 0:
                            clientes_siendo_atendidos -= 1
                        box.cliente.set_cliente_fue_atendido()
                        self.clientes_fueron_atendidos.append(box.cliente) 
                        box.free_box()
                        # print("Se libero el box")
            
            if self.cola:
                if not self.cola[-1].cliente_seguir_esperando(instante_tiempo):
                    cliente_no_atendido = self.cola.pop()
                    self.clientes_no_fueron_atendidos.append(cliente_no_atendido)
                    # print("paso 30 min, cliente se va ", cliente_no_atendido.__dict__.items())
                else:
                    # si hay clientes en espera, se verifica si hay lugar en los boxes
                    for box in self.boxes:
                        if box.status:
                            cliente = self.cola.pop()
                            box.lock_box(cliente)
                            cliente.set_cliente_siendo_atendido(instante_tiempo)
                            # print(cliente.__dict__.items())

            escritor_csv.writerow([instante_tiempo, len(self.clientes), len(self.cola), clientes_siendo_atendidos, 
                                len(self.clientes_fueron_atendidos), len(self.clientes_no_fueron_atendidos),
                                   ])

        archivo_instante.close()

        self.calcular_tiempo_max_min()

        print("\nResumen final:")
        print(f"Total de clientes que ingresaron: {len(self.clientes)}")
        print(f"Clientes atendidos: {len(self.clientes_fueron_atendidos)}")
        print(f"Clientes no atendidos: {len(self.clientes_no_fueron_atendidos)}")
        print(f"Clientes en cola: {len(self.cola)}")
        print(f"Costo total de dinero: {self.calcular_perdida_total()}")
        print(f"Tiempo máximo de atención: {self.tiempo_maximo_atencion}")
        print(f"Tiempo mínimo de atención: {self.tiempo_minimo_atencion}")
        print(f"Tiempo mínimo de espera: {self.tiempo_minimo_espera}")
        print(f"Tiempo máximo de espera: {self.tiempo_maximo_espera}")

        with open("resultado_simulacion.csv", mode='w', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            # Escribir encabezados
            escritor_csv.writerow(['CantidadBoxes', 'Total de clientes que ingresaron', "Clientes atendidos", 'Clientes no atendidos',
                                   "Costo total de dinero", "Tiempo máximo de atención", "Tiempo mínimo de atención",
                                   "Tiempo mínimo de espera", "Tiempo máximo de espera",
                                   ])
            
            escritor_csv.writerow([self.cantidad_boxes, len(self.clientes), len(self.clientes_fueron_atendidos), 
                                   len(self.clientes_no_fueron_atendidos),self.perfida_total, self.tiempo_maximo_atencion, 
                                   self.tiempo_minimo_atencion, self.tiempo_minimo_espera, self.tiempo_maximo_espera,
                                   ])


def main():
    pass

if __name__ == "__main__":
    local = Local()
    local.set_parametros()
    local.set_tiempo_trabajo()
    local.simulacion()
