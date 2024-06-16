import random
import matplotlib.pyplot as plt
# Definir la probabilidad del suceso
probabilidad = 1 / 144

# Definir el intervalo (número de intentos)
tiempo_trabajo = 4*60*60  # Puedes ajustar este número según tus necesidades

# Contar el número de veces que ocurre el suceso
clientes = 0

# Simulación del tiempo_trabajo
for _ in range(tiempo_trabajo):
    if random.random() < probabilidad:
        clientes += 1

print(f"El suceso ocurrió {clientes} veces en {tiempo_trabajo} intentos.")

media = 7200
desviacion_estandar = 7200

# Calcular los límites superior e inferior
limite_inferior = media - desviacion_estandar
limite_superior = media + desviacion_estandar

numeros_generados = set()

# Función para generar un número aleatorio dentro del intervalo dado y convertirlo a entero
def generar_numero_normal_limitedo_entero_unico(media, desviacion_estandar, limite_inferior, limite_superior):
    while True:
        numero = random.normalvariate(media, desviacion_estandar)
        numero_entero = round(numero)  # Convertir el número a entero
        if limite_inferior <= numero_entero <= limite_superior and numero_entero not in numeros_generados:
            numeros_generados.add(numero_entero)
            return numero_entero

# Generar un número aleatorio
instante_entra_cliente = [generar_numero_normal_limitedo_entero_unico(media, desviacion_estandar, limite_inferior, limite_superior) for _ in range(clientes)]

suceso_instante = []

for i in range(tiempo_trabajo):
    if i in instante_entra_cliente:
        suceso_instante.append(True)
    else:
        suceso_instante.append(False)

print(suceso_instante.count(True))
print(len(suceso_instante))

conteos = []
intervalo = 3600
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