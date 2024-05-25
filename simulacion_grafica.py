import datetime
import time
import pygame
import random
import csv

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 1280
ALTO = 720
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Animación de Cuadros')

# Colores
NEGRO = (0, 0, 0)
NARANJA = (255, 165, 0)  # Color naranja
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VIOLETA = (148, 0, 211)
CIAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Fuente para el texto
fuente = pygame.font.Font(None, 24)

# Función para dibujar una línea de cuadros
def dibujar_linea(cantidad_rojos, cantidad_verdes, cantidad_violetas, tiempo, clientes_ya_atendidos, clientes_no_atendidos, texto_resultados):
    tamaño_cuadro = ANCHO // 20
    separacion = tamaño_cuadro // 2

    # Calcular posición inicial de la fila de cuadros
    inicio_x = ((ANCHO - ((tamaño_cuadro + separacion) * 10 - separacion)) // 2) + tamaño_cuadro  # Ajuste para mover hacia la derecha
    inicio_y = ALTO // 6 + tamaño_cuadro  # Ajuste para mover hacia abajo

    # Calcular posición de los círculos y textos
    inicio_x_texto = tamaño_cuadro // 4
    inicio_y_texto = tamaño_cuadro // 4
    radio_circulo = tamaño_cuadro // 4

    # Dibujar círculo verde (box libre) y texto
    pygame.draw.circle(ventana, VERDE, (inicio_x_texto, inicio_y_texto), radio_circulo)
    texto_libre = fuente.render("Box Libre", True, VERDE)
    ventana.blit(texto_libre, (inicio_x_texto + radio_circulo * 2, inicio_y_texto))  # Posición del texto

    # Dibujar círculo naranja (box ocupado) y texto
    pygame.draw.circle(ventana, NARANJA, (inicio_x_texto, inicio_y_texto + tamaño_cuadro // 2 + radio_circulo * 2), radio_circulo)
    texto_ocupado = fuente.render("Box Ocupado", True, NARANJA)
    ventana.blit(texto_ocupado, (inicio_x_texto + radio_circulo * 2, inicio_y_texto + tamaño_cuadro // 2 + radio_circulo * 2))  # Posición del texto

    # Dibujar fila de recuadros
    texto_cola_de_espera = fuente.render("Cola de Espera: " + str(cantidad_violetas) + " personas", True, VIOLETA)
    ventana.blit(texto_cola_de_espera, (10, inicio_y_texto + inicio_y-30))  # Posición del texto

    lineas_resultado = texto_resultados.split('\n')
    x, y = inicio_y_texto, inicio_y+70
    for linea in lineas_resultado:
        texto_resultado = fuente.render(linea, True, MAGENTA)
        ventana.blit(texto_resultado, (x, y))
        y += texto_resultado.get_height()

    texto_ya_atendidos = fuente.render("Clientes ya atendidos(exitosamente): " + str(clientes_ya_atendidos) + " personas", True, CIAN)
    ventana.blit(texto_ya_atendidos, (10, inicio_y_texto + inicio_y*3 - inicio_y // 2))  # Posición del texto

    texto_no_atendidos = fuente.render("Clientes NO atendidos(se fueron): " + str(clientes_no_atendidos) + " personas", True, ROJO)
    ventana.blit(texto_no_atendidos, (10, inicio_y_texto + inicio_y*3))  # Posición del texto

    
    texto_tiempo = fuente.render("Tiempo de simulacion transcurrido (HH:MM:SS) : " + tiempo, True, NARANJA)
    ventana.blit(texto_tiempo, (ANCHO // 2, inicio_y_texto))  # Posición del texto

    for i in range(cantidad_violetas):
        pygame.draw.circle(ventana, VIOLETA, (inicio_x - (i + 1) * (tamaño_cuadro // 2 + separacion // 2) + tamaño_cuadro // 4, inicio_y + tamaño_cuadro // 2), 13)
    for i in range(cantidad_rojos):
        pygame.draw.rect(ventana, NARANJA, (inicio_x + (i + 1) * (tamaño_cuadro + separacion), inicio_y, tamaño_cuadro, tamaño_cuadro))
        pygame.draw.circle(ventana, AZUL, (inicio_x + (i + 1) * (tamaño_cuadro + separacion) + tamaño_cuadro // 2, inicio_y + tamaño_cuadro // 2), 13)  # Aumentar el radio del círculo

    for i in range(cantidad_verdes):
        pygame.draw.rect(ventana, VERDE, (inicio_x + (i + cantidad_rojos + 1) * (tamaño_cuadro + separacion), inicio_y, tamaño_cuadro, tamaño_cuadro))
    
    for i in range(clientes_ya_atendidos):
        pygame.draw.circle(ventana, CIAN, ((i + 1) * (tamaño_cuadro // 2 + separacion // 2) + tamaño_cuadro // 4, inicio_y*3 -inicio_y //2 + tamaño_cuadro), 13)

    for i in range(clientes_no_atendidos):
        pygame.draw.circle(ventana, ROJO, ((i + 1) * (tamaño_cuadro // 2 + separacion // 2) + tamaño_cuadro // 4, inicio_y*3 + tamaño_cuadro), 13)

# Ciclo principal de la animación
reloj = pygame.time.Clock()

with open("resultado_simulacion.csv", mode='r', newline='') as archivo:
    lector_csv = csv.reader(archivo)
    # 1 tot cli 4 costo total 5 max_atencion 6 min atenc 7 min esp 8 max espera
    # Saltar la primera fila (encabezados)
    next(lector_csv)
    segunda_fila = next(lector_csv)
    cantidad_boxes = int(segunda_fila[0])
    cant_total_clientes = int(segunda_fila[1])
    costo_total = int(segunda_fila[4])
    tiempo_max_atencion_box = int(segunda_fila[5])
    tiempo_max_espera_cola = int(segunda_fila[8])

    texto_resultados = (f"Resultados finales: \nCantidad total de clientes: {str(cant_total_clientes)}" +
                        f"\nCosto total: ${str(costo_total)}" + 
                        f"\nTiempo máximo de atencion en Box: {str(tiempo_max_atencion_box//60)} minutos" + 
                        f"\nTiempo máximo espera en cola: {str(tiempo_max_espera_cola//60)} minutos")

ejecutando = True

archivo = open("resultado_instante.csv", mode='r')

# Crear el objeto lector CSV
lector_csv = csv.reader(archivo)
# Saltar la fila de encabezado
fila = next(lector_csv)
while ejecutando:
    try:
        fila = next(lector_csv)
    except:
        pass
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    tiempo = str(datetime.timedelta(seconds=int(fila[0])))
    clientes_ya_atendidos = int(fila[4])
    clientes_no_atendidos = int(fila[5])
    cantidad_rojos = int(fila[3]) #Box ocupados
    cantidad_violetas = int(fila[2]) #Cant en cola de espera
    cantidad_verdes = cantidad_boxes - cantidad_rojos #Box libre es cant de box - los ocupados
    # Leer un conjunto de datos (aquí lo simulamos con números aleatorios)
    ventana.fill(NEGRO)

    # Dibujar la línea de cuadros
    dibujar_linea(cantidad_rojos, cantidad_verdes, cantidad_violetas, tiempo, clientes_ya_atendidos, clientes_no_atendidos, texto_resultados)

    # Actualizar la pantalla
    pygame.display.flip()

    # Esperar un poco antes de la próxima iteración
    time.sleep(0.00001)

    # Controlar la tasa de fotogramas
    reloj.tick(240)

# Cerrar pygame
pygame.quit()
