# # Leer el contenido del archivo modificado
# with open('perm.txt', 'r') as archivo_modificado:
#     contenido_modificado = archivo_modificado.readlines()

# # Leer el contenido del otro archivo y extraer la segunda columna
# with open('TOC实测.txt', 'r') as otro_archivo:
#     contenido_otro = [linea.strip().split()[1] for linea in otro_archivo.readlines()]

# # Determinar la longitud mínima de los contenidos
# longitud_minima = min(len(contenido_modificado), len(contenido_otro))

# # Abrir un nuevo archivo para escribir el contenido con la nueva columna
# with open('archivo_final.txt', 'w') as archivo_final:
#     for i in range(longitud_minima):
#         # Eliminar el salto de línea de la línea del archivo modificado
#         linea_modificada = contenido_modificado[i].strip()
#         # Agregar el dato de la otra columna al final de la línea
#         dato_otro = contenido_otro[i]
#         nueva_linea = f"{linea_modificada} {dato_otro}\n"
#         # Escribir la nueva línea en el archivo final
#         archivo_final.write(nueva_linea)
        
        
        
# Abre el archivo de entrada en modo lectura
with open('permeability.txt', 'r') as archivo_entrada:
    # Lee el contenido del archivo
    contenido = archivo_entrada.read()

# Reemplaza las comas por puntos
contenido_modificado = contenido.replace(',', '.')

# Abre un nuevo archivo en modo escritura
with open('porosity(1).txt', 'w') as archivo_salida:
    # Escribe el contenido modificado en el nuevo archivo
    archivo_salida.write(contenido_modificado)

print("Archivo modificado creado con éxito.")

# Nombre de los archivos de entrada y salida
# archivo_datos = 'porosity(1).txt'
# archivo_destino = 'data.txt'
# archivo_salida = 'data(2).txt'

# # Leer datos del archivo de entrada
# datos = []
# with open(archivo_datos, 'r') as f_datos:
#     for linea in f_datos:
#         datos.append(linea.strip().split())  # Suponiendo que los datos están separados por espacios

# # Leer contenido del archivo destino y reemplazar la columna 1
# nuevo_contenido = []
# with open(archivo_destino, 'r') as f_destino:
#     for linea_destino, linea_datos in zip(f_destino, datos):
#         partes = linea_destino.strip().split()  # Suponiendo que las columnas están separadas por espacios
#         partes[1] = linea_datos[0]  # Reemplazar la primera columna con los datos del archivo de entrada
#         nueva_linea = ' '.join(partes)
#         nuevo_contenido.append(nueva_linea)

# # Escribir el nuevo contenido en el archivo de salida
# with open(archivo_salida, 'w') as f_salida:
#     for linea in nuevo_contenido:
#         f_salida.write(linea + '\n')

# print("Nuevo archivo creado con éxito.")