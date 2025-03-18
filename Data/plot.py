import matplotlib.pyplot as plt
import numpy as np
import os

# Cargar los datos desde el archivo datafinal.txt
data = np.loadtxt('datafinal.txt')

# Obtener los datos específicos de cada columna
depth = data[:, 0]
print(depth)
permeability = data[:, 1] / 1.0e-15
porosity = data[:, 2]
Gas = data[:, 3]
Water = data[:, 4]
LightOil = data[:, 5]
HeavyOil = data[:, 6]
Kerogen = data[:, 7]

# Función para graficar un perfil de pozo
def plot_perfil(ax, data_column, label, ylabel='', show_depth=False):
    color = ''
    linestyle = '-'
    
    if label == 'Gas':
        color = 'green'
        xlim = (0.0, 1.0)
    elif label == 'Water':
        color = 'blue'
        xlim = (0, 1.0)
    elif label == 'Light Oil':
        color = 'orange'
        xlim = (0, 1.0)
    elif label == 'Heavy Oil':
        color = 'red'
        xlim = (0.0, 1.0)
    elif label == 'Kerogen':
        color = 'black'
        xlim = (0.0, 1)
    elif label == 'Permeability':
        color = 'black'
        linestyle = '--'
        xlim = (0.0, 0.5)  # Limitar permeabilidad de 0.01 a 1 mD
    elif label == 'Porosity':
        color = 'black'
        xlim = (0, 0.2)
    
    ax.plot(data_column, depth, label=label, color=color, linestyle=linestyle)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(label)
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('top')  # Configurar la posición de los ticks del eje x en la parte superior)
    ax.set_xlim(xlim)
    ax.set_xticks([xlim[0], xlim[1]])
    if not show_depth:
        
        ax.set_yticklabels([])  # Eliminar las etiquetas del eje y si no es el primer gráfico
        
    ax.invert_yaxis()  # Invertir el eje y


# Crear subgráficos para cada dato
fig, axs = plt.subplots(1, 7, figsize=(10, 6))

plot_perfil(axs[0], Gas, 'Gas', 'Depth (m)', show_depth=True)
plot_perfil(axs[1], Water, 'Water', show_depth=False)
plot_perfil(axs[2], LightOil, 'Light Oil', show_depth=False)
plot_perfil(axs[3], HeavyOil, 'Heavy Oil', show_depth=False)
plot_perfil(axs[4], Kerogen, 'Kerogen', show_depth=False)
plot_perfil(axs[5], permeability, 'Permeability', show_depth=False)
plot_perfil(axs[6], porosity, 'Porosity', show_depth=False)

plt.tight_layout()
# plt.show()

save_path =os.path.join(os.getcwd(), f'data.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
