from Ecuaciones import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
#np.set_printoptions(precision=4, suppress=True)

# Materiales
fc = 20
fy = 420
phi = 0.65

# Refuerzo
Ref_long = '5/8'            # Diametro de las barras long _ [cm]
Estribos = '3/8'            # Diametro de los estribos _ [cm]
n_Asy = 4                   # Numero de barras por cara dir y
n_Asx = 3                   # Numero de barras por cara dir x
pmin = 0.02                 # Cuantía mínima en columnas 1.0 %

# Geometria
b = 25                      # Base de la columna _ [cm]
h = 35                      # Altura de la columna _ [cm]
r = 4.0                     # Recubrimiento del refuerzo _ [cm]
L = 3.10                    # Altura libre de la columna _ [m]

# Cargas y momentos de diseño
Capacidad = 'DMO'           # Capacidad de disipacion DMI, DMO, DES.
Pu = np.array([85, 74])
Mux = np.array([40, 46])
Muy = np.array([38, 29])

# Desarrollo
db = f_db(Ref_long)         # Diametro de las barras long _ [cm]
de = f_db(Estribos)         # Diametro de los estribos _ [cm]
Asb = f_Asb(Ref_long)       # Area de las barras long _ [cm²]
d = h - r - de - db/2       # Altura efectiva
Pud = np.max(Pu)            # Caraga axial máxima
Muxd = np.max(Mux)          # Momento de diseño máximo dir "x"
Muyd = np.max(Muy)          # Momento de diseño máximo dir "y"


# ======================================================================== #
# Área sección bruta y refuerzo
Asmin = pmin * b * h
cant = (2 * n_Asy) + (2 * n_Asx) - 4
Astot = cant * Asb
Pn = Carga_axial(b, h, fc, fy, phi, Astot)
if (Pn >= Pud):
    Pn_mayor_Pu = 'Ok'
else:
    Pn_mayor_Pu = 'No cumple'


# ======================================================================== #
# Refuerzo trasversal
Dist1, Dist2 = Dis_Cortante(Capacidad, db, de, b, h, L)
Est_zona1 = Dist1
Est_zona2 = Dist2


# ======================================================================== #
# Datos para el diagrama para momento Mx
[Rx] = Diagrama(h, fc, b, n_Asy, r, de, db, n_Asx, Asb, fy)
dfx = pd.DataFrame(Rx, columns=["C", "Mn", "Pn", "øMnx", "øPn"])

# Datos para el diagrama para momento My
[Ry] = Diagrama(b, fc, h, n_Asx, r, de, db, n_Asy, Asb, fy)
dfy = pd.DataFrame(Ry, columns=["C", "Mn", "Pn", "øMny", "øPn"])

dfr = pd.concat([dfx[["C", "øPn", "øMnx"]], dfy[["øMny"]]], axis=1)
#print(dfr.head())


# ======================================================================== #
# Reporte
P1 = 'Diseño Columnas '
P2 = 'Materiales '
P3 = 'fc: Resistencia del concreto'
P4 = 'fy: Fluencia del acero'
P5 = 'ø: Coef. Reducción de resistencia '
P6 = ' '
P7 = 'Geometria '
P8 = 'bw: Base '
P9 = 'h: Altura '
P10 = 'r: Recubrimiento '
P11 = 'L: Altura libre de la columna'
P12 = ' '
P13 = 'Refuerzo longitudinal '
P14 = 'pmin: Cuantía mínima'
P15 = 'Asmin: Acero mínimo '
P16 = 'Barra'
P17 = 'Cantidad'
P18 = 'Ast: Acero total'
P19 = ' '
P20 = 'Refuerzo transversal '
P21 = 'Disipación de energia'
P22 = 'dbe : Diámetro estribos'
P23 = 'Estribos en zona confinada'
P24 = 'Estribos en zona no confinada'
P25 = ' '
P26 = 'Resistencia a carga axial '
P27 = 'øPn: Resistencia nominal carga axial'
P28 = 'Pu: Carga axial de diseño'
P29 = 'øPn > Pu'
P30 = ' '
P31 = 'Diseño a flexo-compresión. '
P32 = 'Pu: Max. carga axial de diseño'
P33 = 'Mux: Max momento de diseño dir "x"'
P34 = 'Muy: Max momento de diseño dir "y"'

V1 = ' '
V2 = ' '
V3 = fc
V4 = fy
V5 = phi
V6 = ' '
V7 = ' '
V8 = b
V9 = h
V10 = r
V11 = L
V12 = ' '
V13 = ' '
V14 = pmin
V15 = Asmin
V16 = Ref_long
V17 = cant
V18 = round(Astot, 2)
V19 = ' '
V20 = ' '
V21 = Capacidad
V22 = Estribos
V23 = Est_zona1
V24 = Est_zona2
V25 = ' '
V26 = ' '
V27 = round(Pn, 2)
V28 = Pud
V29 = Pn_mayor_Pu
V30 = ' '
V31 = ' '
V32 = Pud
V33 = Muxd
V34 = Muyd

U1 = ''
U2 = ''
U3 = '[Mpa]'
U4 = '[Mpa]'
U5 = ''
U6 = ''
U7 = ''
U8 = '[cm]'
U9 = '[cm]'
U10 = '[cm]'
U11 = '[m]'
U12 = ''
U13 = ''
U14 = ''
U15 = '[cm²]'
U16 = '[in]'
U17 = '[un]'
U18 = '[cm²]'
U19 = ''
U20 = ''
U21 = ''
U22 = '[in]'
U23 = ''
U24 = ''
U25 = ''
U26 = ''
U27 = '[kN]'
U28 = '[kN]'
U29 = ''
U30 = ''
U31 = ''
U32 = '[kN]'
U33 = '[kN.m]'
U34 = '[kN.m]'

parametro = np.array([P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24,P25,P26,P27,P28,P29,P30,P31,P32,P33,P34])
unidad = np.array([U1,U2,U3,U4,U5,U6,U7,U8,U9,U10,U11,U12,U13,U14,U15,U16,U17,U18,U19,U20,U21,U22,U23,U24,U25,U26,U27,U28,U29,U30,U31,U32,U33,U34])
valor= np.array([V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,V29,V30,V31,V32,V33,V34])

print('\nDISEÑO COLUMNAS RECTANGULARES')
print('---------------------------------------------------------------')
datos = {'PARÁMETRO': parametro,'UNIDAD': unidad, 'VALOR': valor}
df = pd.DataFrame(datos)
#print(df.head())
print (df.loc[1:])

# Datos guardados en excel
with pd.ExcelWriter('D:\APP_REPORTES\Reporte_Columnas.xlsx') as writer:
    df.to_excel(writer, sheet_name='Columna', index=False, float_format="%.2f")
    dfr.to_excel(writer, sheet_name='Interación', index=False, float_format="%.2f")
print ('\n!!! Datos guardados con exitos ¡¡¡')


# ======================================================================== #
# GRAFICAS ASOCIADAS
# Diagrama de interaacion Pn - Mnx
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)

xmax = np.amax(Rx[:, 1])
ymax = np.amax(Rx[:, 2])
ymin = np.amin(Rx[:, 2])

x1 = [0, 0]
y1 = [ymin, ymax]
x2 = [0, xmax]
y2 = [0, 0]

plt.plot(x1, y1, '-.', color='brown')
plt.plot(x2, y2, '-.', color='brown')

plt.title('Diagrama de interacción Pn -Mnx', fontsize = 10)
plt.xlabel('Momento dir "x" _ [kN.m]', fontsize = 9)
plt.ylabel('Carga axial _ [kN]', fontsize = 9)
plt.plot(Rx[:, 1], Rx[:, 2], '-', color='black')
plt.plot(Rx[:, 3], Rx[:, 4], '--', color='blue')

# Gráfica de cargas
plt.scatter(Mux, Pu, color='red', marker='.')
plt.grid(color='gray', linestyle=':')


# ======================================================================== #
# Diagrama de interaacion Pn - Mny
plt.subplot(1, 2, 2)
xmax = np.amax(Rx[:, 1])
ymax = np.amax(Rx[:, 2])
ymin = np.amin(Rx[:, 2])

x1 = [0, 0]
y1 = [ymin, ymax]
x2 = [0, xmax]
y2 = [0, 0]

plt.plot(x1, y1, '-.', color='brown')
plt.plot(x2, y2, '-.', color='brown')

plt.title('Diagrama de interacción Pn -Mny', fontsize = 10)
plt.xlabel('Momento dir "y" _ [kN.m]', fontsize = 9)
plt.ylabel('Carga axial _ [kN]', fontsize = 9)
plt.plot(Ry[:, 1], Ry[:, 2], '-', color='black')
plt.plot(Ry[:, 3], Ry[:, 4], '--', color='blue')

# Gráfica de cargas
plt.scatter(Muy, Pu, color='red', marker='.')
plt.grid(color='gray', linestyle=':')

plt.tight_layout()          # Ajustar automáticamente el espaciado
plt.show()


# ======================================================================== #
# Grafica seccion trasversal de la columna

# Crea una figura y un eje
fig, ax = plt.subplots()

#Crea un rectángulo utilizando la clase patches.Rectangle
Col = patches.Rectangle((0, 0), b, h, linewidth=1.5, edgecolor='black', facecolor='#F8ECE0')
Est = patches.Rectangle((r, r), (b - 2 * r), (h - 2 * r), linewidth=3, edgecolor='r', facecolor='none')

# Agrega el rectángulo que grafica la columan y el estribo
ax.add_patch(Col)
ax.add_patch(Est)

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