import numpy as np
import matplotlib.pyplot as plt
def generar_numeros_normal_enteros(n, media, desviacion_estandar, min_valor, max_valor):
    # Generar números aleatorios con distribución normal
    valores = np.random.normal(media, desviacion_estandar, n)
    

    
    # Redondear los valores a enteros
    valores_enteros = np.round(valores).astype(int)
    
    return valores_enteros

# Parámetros
n = 10000  # número de elementos en el conjunto
media = 7200
desviacion_estandar = 7200
min_valor = 0
max_valor = 14400

# Generar el conjunto de números
numeros_generados = generar_numeros_normal_enteros(n, media, desviacion_estandar, min_valor, max_valor)

# Mostrar los números generados
print(numeros_generados)

# Graficar los números generados
plt.figure(figsize=(10, 6))
plt.hist(numeros_generados, bins=30, edgecolor='black')
plt.title('Histograma de Números Generados con Distribución Normal')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.show()