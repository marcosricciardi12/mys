import datetime
import random
import numpy as np

def validar_horario_convertir(horario):
    try:
        hora_min = horario.split(":")
        hora = int(hora_min[0])
        minutos = int(hora_min[1])
        if 0 <= hora <= 23 and 0 <= minutos <= 59:
            horario_date = datetime.time(hora, minutos, 0)
            return True, horario_date
        else:
            return False, None
    except ValueError:
        return False, None

def setear_horario():
    while True:
        input_hora = input("Ingrese hora (Formato de 24hrs tipo HH:MM): ")
        hora_valida, horario_date = validar_horario_convertir(input_hora)
        if not hora_valida:
            print("Formato de hora inválido, intente nuevamente")
        else:
            fecha_sistema = datetime.datetime.now().date()
            horario_date = datetime.datetime.combine(fecha_sistema, horario_date)
            return horario_date

def suceso_cliente_ingresa(probabilidad):
    numero_aleatorio = random.random()
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
        self.tiempo_atencion = int(np.random.normal(10, 5) * 60)

    def set_cliente_fue_atendido(self):
        self.siendo_atendido = False
        self.fue_atendido = True

    def terminar_atencion(self, tiempo_instante_actual):
        if tiempo_instante_actual - self.instante_comienzo_atencion_box >= self.tiempo_atencion:
            self.set_cliente_fue_atendido()
            return True
        else:
            return False

    def cliente_seguir_esperando(self, instante_actual):
        if instante_actual - self.instante_ingreso_local >= self.tiempo_espera_max:
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
        self.probabilidad_cliente = 1 / 144

    def set_cant_boxes(self):
        while True:
            try:
                input_boxes = int(input("Ingrese la cantidad de boxes (1-10): "))
                if input_boxes <= 0 or input_boxes > 10:
                    raise ValidarBoxesError("Cantidad invalida, debe ser mayor a 0 y menor o igual que 10")
                else:
                    return input_boxes
            except (ValueError, ValidarBoxesError) as e:
                print(e)

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
        for instante_tiempo in range(self.tiempo_trabajo):
            if suceso_cliente_ingresa(self.probabilidad_cliente):
                self.ingreso_cliente(instante_tiempo)
                
            for box in self.boxes:
                if box.cliente is not None:
                    if box.cliente.terminar_atencion(instante_tiempo):
                        box.cliente.set_cliente_fue_atendido()
                        self.clientes_fueron_atendidos.append(box.cliente) 
                        box.free_box()
                        print("Se libero el box")
            
            if self.cola:
                for box in self.boxes:
                    if box.status and self.cola:
                        cliente = self.cola.pop()
                        box.lock_box(cliente)
                        cliente.set_cliente_siendo_atendido(instante_tiempo)
                        print("Cliente atendido desde la cola: ", cliente.__dict__.items())
                        break

        print("\nSimulación completada")
        print(f"Total de clientes: {len(self.clientes)}")
        print(f"Clientes atendidos: {len(self.clientes_fueron_atendidos)}")
        print(f"Clientes no atendidos: {len(self.clientes_no_fueron_atendidos)}")
        print(f"Clientes en cola: {len(self.cola)}")
        print("\nEstado de los boxes al finalizar la simulación:")
        for box in self.boxes:
            if box.cliente is not None:
                print(f"Box {box.box_numero} ocupado por: {box.cliente.__dict__.items()}")

        instante_tiempo = self.tiempo_trabajo

        while self.cola:
            instante_tiempo += 1
            if not self.cola[-1].cliente_seguir_esperando(instante_tiempo):
                cliente_no_atendido = self.cola.pop()
                self.clientes_no_fueron_atendidos.append(cliente_no_atendido)
                print("Pasaron 30 min, cliente se va: ", cliente_no_atendido.__dict__.items())
            else:
                for box in self.boxes:
                    if box.status:
                        cliente = self.cola.pop()
                        box.lock_box(cliente)
                        cliente.set_cliente_siendo_atendido(instante_tiempo)
                        print("Cliente atendido desde la cola fuera de horario: ", cliente.__dict__.items())
                        break

        while True:
            instante_tiempo += 1
            todos_box_vacios = True
            for box in self.boxes:
                if box.cliente is not None:
                    todos_box_vacios = False
                    print("Box ocupado fuera de hora por: ", box.cliente.__dict__.items())
                    if box.cliente.terminar_atencion(instante_tiempo):
                        box.cliente.set_cliente_fue_atendido()
                        self.clientes_fueron_atendidos.append(box.cliente) 
                        box.free_box()
                        print("Se libero el box")  
            if todos_box_vacios:
                break

        print("\nResumen final:")
        print(f"Total de clientes: {len(self.clientes)}")
        print(f"Clientes atendidos: {len(self.clientes_fueron_atendidos)}")
        print(f"Clientes no atendidos: {len(self.clientes_no_fueron_atendidos)}")
        print(f"Clientes en cola: {len(self.cola)}")

def main():
    local = Local()
    local.set_parametros()
    local.set_tiempo_trabajo()
    local.simulacion()

if __name__ == "__main__":
    main()
