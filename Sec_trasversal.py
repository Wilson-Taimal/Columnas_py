import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Ecuaciones import *

# Refuerzo
Ref_long = '5/8'            # Diametro de las barras long _ [cm]
Estribos = '3/8'            # Diametro de los estribos _ [cm]
n_Asy = 4                   # Numero de barras por cara dir y
n_Asx = 3                   # Numero de barras por cara dir x

# Geometria
b = 40                      # Base de la columna _ [cm]
h = 50                      # Altura de la columna _ [cm]
r = 4.0                     # Recubrimiento del refuerzo _ [cm]
L = 3.10                    # Altura libre de la columna _ [m]

# Desarrollo
db = f_db(Ref_long)         # Diametro de las barras long _ [cm]
de = f_db(Estribos)         # Diametro de los estribos _ [cm]
Asb = f_Asb(Ref_long)       # Area de las barras long _ [cm²]
d = h - r - de - db/2       # Altura efectiva


# Crea una figura y un eje
fig, ax = plt.subplots()

#Crea un rectángulo utilizando la clase patches.Rectangle
Col = patches.Rectangle((0, 0), b, h, linewidth=1.5, edgecolor='black', facecolor='#F8ECE0')
Est = patches.Rectangle((r, r), (b - 2 * r), (h - 2 * r), linewidth=3, edgecolor='r', facecolor='none')

# Agrega el rectángulo al eje
ax.add_patch(Col)
ax.add_patch(Est)
#ax.add_patch(Bar)

for i in range(n_Asx):
    x = r + de + db / 2 + i * (b - 2 * (r + de + db / 2)) / (n_Asx - 1)
    y_top = r + de + db / 2
    y_bottom = h - (r + de + db / 2)
    circle_top = patches.Circle((x, y_top), db / 2, linewidth=1, edgecolor='black', facecolor='grey')
    circle_bottom = patches.Circle((x, y_bottom), db / 2, linewidth=1, edgecolor='black', facecolor='grey')
    ax.add_patch(circle_top)
    ax.add_patch(circle_bottom)

for i in range(n_Asy):
    y = r + de + db / 2 + i * (h - 2 * (r + de + db / 2)) / (n_Asy - 1)
    x_left = r + de + db / 2
    x_right = b - (r + de + db / 2)
    circle_left = patches.Circle((x_left, y), db / 2, linewidth=1, edgecolor='black', facecolor='grey')
    circle_right = patches.Circle((x_right, y), db / 2, linewidth=1, edgecolor='black', facecolor='grey')
    ax.add_patch(circle_left)
    ax.add_patch(circle_right)

# Establece los límites del eje para que se destaque el rectángulo
ax.set_xlim(-5, b+5)
ax.set_ylim(-5, h+5)
ax.set_aspect('equal')

# Agrega etiquetas y título
plt.xlabel('Base _ [cm]')
plt.ylabel('Altura _ [cm]')
plt.title(f'Columna {b} x {h} cm')

# Agregar texto al gráfico
cant = (2 * n_Asy) + (2 * n_Asx) - 4
plt.text(b/2, h/2+2, f'Ref log: {cant} ø {Ref_long}', ha='center', fontsize=8)
plt.text(b/2, h/2-2, f'Estribos ø {Estribos} ', ha='center', fontsize=8)

# Muestra el gráfico
plt.grid(color='gray', linestyle=':')
plt.show()