# # Leer el contenido del archivo 1
# with open('data.txt', 'r') as file:
#     lines1 = file.readlines()

# # Leer el contenido del archivo 2
# with open('data - Copy.txt', 'r') as file:
#     lines2 = file.readlines()

# # Sustituir la columna 2 de lines1 por la columna 8 de lines2
# for i, line in enumerate(lines2):
#     parts = line.split()  # Separar la línea en partes
#     if len(parts) > 8:  # Verificar si hay suficientes columnas
#         lines1[i] = '\t'.join(parts[:7] + [parts[8]]) + '\n'  # Sustituir la columna 2 por la columna 8

# # Guardar el resultado en un nuevo archivo
# with open('resultado.txt', 'w') as file:
#     file.writelines(lines1)

# print("Proceso completado. El archivo resultante se ha guardado como resultado.txt")

# import numpy as np

# # Cargar los datos desde data.txt
# data1 = np.loadtxt('data.txt')

# # Cargar los datos desde data(2).txt
# data2 = np.loadtxt('data(2).txt')

# # Seleccionar las columnas específicas de cada archivo
# data1_seleccionadas = data1[:, [0, 7, 8]]  # Columnas 1, 9 y 10 de data.txt
# data2_seleccionadas = data2[:, 2:7]  # Columnas 3 a 7 de data(2).txt

# # Combinar las columnas seleccionadas en un solo array
# data_final = np.concatenate((data1_seleccionadas, data2_seleccionadas), axis=1)

# # Guardar los datos en datafinal.txt
# np.savetxt('datafinal.txt', data_final)

# # Abrir el archivo para lectura y escritura
# with open('data.txt', 'r+') as file:
#     # Leer todas las líneas del archivo
#     lines = file.readlines()
    
#     # Extraer la primera profundidad del archivo
#     first_depth = float(lines[0].split()[0])

#     # Calcular cuántas líneas nuevas agregar
#     num_new_lines = int((first_depth - 1818) / 0.15)

#     # Crear las nuevas líneas
#     new_lines = [f"{first_depth - i * 0.15:.18e} 1.0e-17 0.01 0.0 0.0 0.0 0.0 0.0\n" for i in range(1, num_new_lines + 1)]

#     # Escribir las nuevas líneas al inicio del archivo
#     file.seek(0)
#     file.writelines(new_lines[::-1] + lines)

# print(f"Se agregaron {num_new_lines} líneas nuevas al archivo.")

# # Abrir el archivo para lectura y escritura
# with open('data.txt', 'r+') as file:
#     # Leer todas las líneas del archivo
#     lines = file.readlines()
    
#     # Extraer la última profundidad del archivo
#     last_depth = float(lines[-1].split()[0])

#     # Calcular cuántas líneas nuevas agregar
#     num_new_lines = int((1843 - last_depth) / 0.15)

#     # Crear las nuevas líneas
#     new_lines = [f"{last_depth + i * 0.15:.18e} 1.0e-16 0.01 0.0 0.0 0.0 0.0 0.0\n" for i in range(1, num_new_lines + 1)]

#     # Escribir las nuevas líneas al final del archivo
#     file.seek(0, 2)
#     file.writelines(new_lines)

# print(f"Se agregaron {num_new_lines} líneas nuevas al final del archivo.")# Abrir el archivo para lectura y escritura


# with open('data.txt', 'r+') as file:
#     # Leer todas las líneas del archivo
#     lines = file.readlines()
    
#     # Extraer la última profundidad del archivo
#     last_depth = float(lines[-1].split()[0])

#     # Calcular cuántas líneas nuevas agregar
#     num_new_lines = int((1843 - last_depth) / 0.15)

#     # Crear las nuevas líneas
#     new_lines = [f"{last_depth + i * 0.15:.18e} 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n" for i in range(1, num_new_lines + 1)]

#     # Escribir las nuevas líneas al final del archivo
#     file.seek(0, 2)
#     file.writelines(new_lines)

# print(f"Se agregaron {num_new_lines} líneas nuevas al final del archivo.")


import os
import numpy as np
data_path = os.path.join(os.getcwd(), 'data.txt')
data = np.loadtxt(data_path)

y = data[:, 0]
y = (-(y[0] - y[1:]))
y = np.insert(y, 0, 0)
print(len(y))