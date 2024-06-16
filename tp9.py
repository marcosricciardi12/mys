# Se trata de un conducto circular en el que se generan particulas en su centro.
# Las particulas pueden tener dif tamaños
# Las particualas serán cuadradas con lonngitudes de lado variable
# La particula esta dotada de un movimineto aleatorio hacia arriba abajo derecha izq.
# Por cada segundo la particula se movera aleatoriamente.
# Cuando la particula toca el borde del conducto u otra particula, queda fija/adherida a otra particula o al borde.
# En algun momento, la particula tocará el borde u otra particula.
# El conducto comienza vacio, y se larga de una particular en una, de forma que comienza vacio.
# Cada particula comienza en el centro, de forma que en algun momento la cañeria estará obstruida
# Parametros: Forma y area/dimensiones del condcuto. entre 1 y 200mm
# dimension de la particula, entre 1mm y 10mm

import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_size = 640
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Simulación de Conducto")

# Colores
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)

# Función para convertir tamaño real a tamaño en píxeles
def convert_to_pixels(value, min_value=100, max_value=1000, min_pixels=60, max_pixels=600):
    return int(min_pixels + (value - min_value) * (max_pixels - min_pixels) / (max_value - min_value))

# Función para pedir input del usuario
def get_user_input():
    shape = input("Seleccione el conducto (cuadrado/circular): ").strip().lower()
    size = int(input("Ingrese el tamaño del lado/diámetro (100-1000): ").strip())
    square_size = int(input("Ingrese el tamaño de los cuadrados a generar (1-10): ").strip())
    return shape, size, square_size

# Función para dibujar el conducto
def draw_conduit(shape, size, color):
    if shape == "cuadrado":
        top_left = (screen_size // 2 - size // 2, screen_size // 2 - size // 2)
        pygame.draw.rect(screen, color, (*top_left, size, size), 7)
    elif shape == "circular":
        pygame.draw.circle(screen, color, (screen_size // 2, screen_size // 2), size // 2, 7)

# Función para mover un cuadrado de manera aleatoria
def choose_random_direction(last_direction):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if last_direction in directions:
        directions.remove(last_direction)
    return random.choice(directions)

# Función para detectar colisión
def detect_collision(square, shape, size, square_size, fixed_squares):
    if shape == "cuadrado":
        if (square[0] < screen_size // 2 - size // 2 or
            square[0] > screen_size // 2 + size // 2 or
            square[1] < screen_size // 2 - size // 2 or
            square[1] > screen_size // 2 + size // 2):
            return True
    elif shape == "circular":
        radius = size // 2
        distance_to_center = ((square[0] - screen_size // 2) ** 2 + (square[1] - screen_size // 2) ** 2) ** 0.5
        if distance_to_center + square_size // 2 >= radius-7:
            return True

    for fixed_square in fixed_squares:
        if abs(square[0] - fixed_square[0]) < square_size and abs(square[1] - fixed_square[1]) < square_size:
            return True

    return False

# Función para dibujar el cuadrado verde en el centro
def draw_green_square():
    green_square_size = 50
    top_left = (screen_size // 2 - green_square_size // 2, screen_size // 2 - green_square_size // 2)
    pygame.draw.rect(screen, GREEN, (*top_left, green_square_size, green_square_size), 2)

# Función principal de la simulación
def simulation():
    shape, size, square_size = get_user_input()
    size = convert_to_pixels(size)
    square_size = convert_to_pixels(square_size, 1, 10, 1, 60)

    speed = 10  # Velocidad inicial en píxeles por segundo
    clock = pygame.time.Clock()

    fixed_squares = []
    new_square = (screen_size // 2, screen_size // 2)
    last_direction = None
    conduit_color = BLUE

    running = True
    simulation_active = True
    time_since_last_move = 0  # Tiempo desde el último movimiento
    direction = choose_random_direction(last_direction)
    pixels_to_move = speed // 10  # Píxeles a moverse en la dirección actual

    while running:
        screen.fill(BLACK)
        draw_green_square()  # Dibujar el cuadrado verde en el centro

        if simulation_active:
            draw_conduit(shape, size, conduit_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        speed += 10
                    elif event.key == pygame.K_MINUS:
                        speed = max(10, speed - 10)
                    pixels_to_move = speed // 10

            time_since_last_move += clock.get_time()
            if time_since_last_move >= 1000 // speed:
                for _ in range(pixels_to_move):
                    new_square = (new_square[0] + direction[0], new_square[1] + direction[1])
                    if detect_collision(new_square, shape, size, square_size, fixed_squares):
                        fixed_squares.append(new_square)
                        if ((new_square[0] - screen_size // 2) ** 2 + (new_square[1] - screen_size // 2) ** 2) ** 0.5 < 50:
                            simulation_active = False
                            conduit_color = MAGENTA
                        new_square = (screen_size // 2, screen_size // 2)
                        last_direction = direction
                        direction = choose_random_direction(last_direction)
                        break
                else:
                    direction = choose_random_direction(direction)
                time_since_last_move = 0

            for sq in fixed_squares:
                pygame.draw.rect(screen, ORANGE, (sq[0] - square_size // 2, sq[1] - square_size // 2, square_size, square_size), 3)

            pygame.draw.rect(screen, ORANGE, (new_square[0] - square_size // 2, new_square[1] - square_size // 2, square_size, square_size), 3)
        else:
            draw_conduit(shape, size, MAGENTA)

            for sq in fixed_squares:
                pygame.draw.rect(screen, ORANGE, (sq[0] - square_size // 2, sq[1] - square_size // 2, square_size, square_size), 3)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    simulation()
