# ======================================================================== #
def f_db(barra):
    match barra:
        case '1/4':
            db = 0.64
        case '3/8':
            db = 0.95
        case '1/2':
            db = 1.27
        case '5/8':
            db = 1.59
        case '3/4':
            db = 1.91
        case '7/8':
            db = 2.22
        case '1':
            db = 2.54
        case '1-1/8':
            db = 2.87
        case '1-1/4':
            db = 3.23
        case '1-3/8':
            db = 3.58
        case '1-3/4':
            db = 4.30
    return db


# ======================================================================== #
def f_Asb(barra):
    match barra:
        case '1/4':
            Asb = 0.32
        case '3/8':
            Asb = 0.71
        case '1/2':
            Asb = 1.29
        case '5/8':
            Asb = 1.99
        case '3/4':
            Asb = 2.84
        case '7/8':
            Asb = 3.87
        case '1':
            Asb = 5.10
        case '1-1/8':
            Asb = 6.45
        case '1-1/4':
            Asb = 8.19
        case '1-3/8':
            Asb = 10.06
        case '1-3/4':
            Asb = 14.52
    return Asb


# ======================================================================== #
def Carga_axial (b, h, fc, fy, phi, Astot):
    Ag = b * h
    fc = fc/10
    fy = fy/10
    Pn = 0.75 * phi * (0.85*fc*(Ag - Astot) + fy * Astot)
    return Pn


# ======================================================================== #
def Dis_Cortante (Capacidad, db, de, b, h, L):
    if Capacidad == 'DMI':
        Lo = 0
        S1 = 0
        S2 = min((16 * db), (48 * de), b, h)
        Cant1 = 0
        Cant2 = round((L * 100 - 10) / S2 + 1, 0)
        Sr1 = 0
        Sr2 = (L * 100 - 10) / (Cant2 - 1)
        Dist1 = 'No aplica'
        Dist2 = f'{Cant2} Est @ {round(Sr2, 2)} cm'

    elif Capacidad == 'DMO':
        Lo = max((max(b, h)), (L / 6 * 100), 50)
        Lo = round(Lo, 0)
        S1 = min((b / 3), (h / 3), (8 * db), (16 * de), 15)
        S2 = 2 * S1
        Cant1 = round((Lo - 5) / S1 + 1, 0)
        Cant2 = round((L * 100 - 2 * Lo) / S2, 0)
        Sr1 = (Lo - 5) / (Cant1 - 1)
        Sr2 = (L * 100 - 2 * Lo) / (Cant2 + 1)
        Dist1 = f'{Cant1} Est @ {round(Sr1, 2)} cm'
        Dist2 = f'{Cant2} Est @ {round(Sr2, 2)} cm'

    else:
        Lo = max((max(b, h)), (L / 6 * 100), 45)
        Lo = round(Lo, 0)
        S1 = min((b / 4), (h / 4), (6 * db), 10)
        S2 = min((6 * db), 15)
        Cant1 = round((Lo - 5) / S1 + 1, 0)
        Cant2 = round((L * 100 - 2 * Lo) / S2, 0)
        Sr1 = (Lo - 5) / (Cant1 - 1)
        Sr2 = (L * 100 - 2 * Lo) / (Cant2 + 1)
        Dist1 = f'{Cant1} Est @ {round(Sr1, 2)} cm'
        Dist2 = f'{Cant2} Est @ {round(Sr2, 2)} cm'

    return Dist1, Dist2


# ======================================================================== #
def Resistecia_Concreto (fc, c, b, h):
    if fc <= 28:
        B1 = 0.85
    elif fc > 28 and fc <= 55:
        B1 = 0.85 - 0.05 * (fc - 28) / 7
    else:
        B1 = 0.65
    a = B1 * c
    Fc = 0.85 * a * b * (fc / 10)       # Fuerza  compresion _ [kN]
    Zc = 0.5 * (h - a)
    Mc = Fc * Zc/100                    # Momento _ [kN.m]
    return Fc, Mc


# ======================================================================== #
def Resistencia_Acero (n_Asy, h, r, de, db, n_Asx, Asb, c, fy, ):
    import numpy as np
    # Resistencia del acero
    M = np.zeros((n_Asy, 9))
    esp = (h - 2 * r - 2 * de - db) / (n_Asy - 1)
    d1 = r + de + db / 2

    for i in range(1, n_Asy + 1):
        # Col 0 Numero de capas
        M[i - 1, 0] = i

        # Col 1 Areas de refuerzo por capa _ [cm²]
        if i == 1 or i == n_Asy:
            M[i - 1, 1] = n_Asx * Asb
        else:
            M[i - 1, 1] = 2 * Asb

        # Col 2 Distancia al centroide de cada barra _ [cm]
        if i == 1:
            M[i - 1, 2] = d1
        else:
            M[i - 1, 2] = d1 + (esp * (i - 1))

        # Col 3 Calculo de la deformacion Esi
        M[i - 1, 3] = 0.003 * (c - M[i - 1, 2]) / c

        # Col 4 Calculo de fsi _ [kN/cm²]
        M[i - 1, 4] = (fy / 10) / 0.002 * M[i - 1, 3]

        # Col 5 Correccion de fsi, fsi no puede ser mayor a fy
        fsi_temp = M[i - 1, 4]
        if M[i - 1, 4] >= (fy / 10):
            M[i - 1, 5] = (fy / 10)
        elif M[i - 1, 4] < -(fy / 10):
            M[i - 1, 5] = (-fy / 10)
        else:
            M[i - 1, 5] = fsi_temp

        # Col 6 Calculo de Fsi _ [kN]
        M[i - 1, 6] = (M[i - 1, 5]) * M[i - 1, 1]

        # Col 7 Calculo Zsi _ [cm]
        M[i - 1, 7] = h / 2 - M[i - 1, 2]

        # Col 8 Calculo de Msi = Fsi * Zsi _ [kN.m]
        M[i - 1, 8] = (M[i - 1, 6] * M[i - 1, 7]) / 100

    np.set_printoptions(precision=4, suppress=True)

    # Calculo factor de reducción
    du = abs(M[n_Asy - 1, 3])
    if du <= 0.002:
        fi_r = 0.65
    elif du > 0.002 and du <= 0.005:
        fi_r = (250 / 3) * du + (29 / 60)
    else:
        fi_r = 0.90

    # Resistencia del acero
    SFsi = np.sum(M[:, 6])
    SMsi = np.sum(M[:, 8])    

    return SFsi, SMsi, fi_r


# ======================================================================== #
def Diagrama (h, fc, b, n_Asy, r, de, db, n_Asx, Asb, fy):
    import numpy as np
    puntos = 100
    c = np.linspace(0.01, 1.2*h, puntos)
    R = np.zeros((puntos, 5))

    for i in range(len(c)):

       # Resistencia del cocreto
        Fc, Mc = Resistecia_Concreto(fc, c[i], b, h)

        # Resistencia del acero
        SFsi, SMsi, fi_r = Resistencia_Acero(n_Asy, h, r, de, db, n_Asx, Asb, c[i], fy, )

        # Reistencia nomimal
        Pn = Fc + SFsi
        Mn = Mc + SMsi

        # Guardar valores
        R[i-1, 0] = c[i]
        R[i-1, 1] = Mn
        R[i-1, 2] = Pn
        R[i-1, 3] = fi_r * Mn
        R[i-1, 4] = fi_r * Pn
    
    c = c[:-1]
    R = R[:-1]

    return [R]