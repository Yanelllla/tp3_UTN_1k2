class Tratamiento:
    def __init__(self, dni, nombre, apellido, icd10, montobase, complejidad, idalgoritmo):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.icd10 = icd10
        self.montobase = montobase
        self.complejidad = complejidad
        self.idalgoritmo = idalgoritmo

    def __str__(self):
        r = "Tratamiento"
        r += f"|DNI:{self.dni:<8}"
        r += f"|Nombre:{self.nombre:<12}"
        r += f"|Apellido:{self.apellido:<12}"
        r += f"|ICD10:{self.icd10:<8}"
        r += f"|Monto Base:{self.montobase:<8}"
        r += f"|Complejidad:{self.complejidad:<4}"
        r += f"|Id algoritmo:{self.idalgoritmo:<4}"
        return r

def porcentaje_normal(tratamientos):
    n = len(tratamientos)

    for i in range(n):
        tratamiento = tratamientos[i]

    punto = tratamiento.icd10.find(".")
    porcentaje_extra = int(tratamiento.icd10[punto + 1:]) / 100

    return porcentaje_extra

def calculonormal(tratamientos):
    ad_al = 25000
    ad_mz = 40000
    ad_u = 100000
    fijo = 25000#Monto fijo establecido en el tp1

    montos_finales = []#lista que contendrá todos los resultados que cumplen la condición.
    n = len(tratamientos)
    for cal in range(n):
        tratamiento = tratamientos[cal]
        if tratamiento.idalgoritmo > 3:

            letra = tratamiento[cal].icd10[0]
            if "A" <= letra <= "L":
                adicional = ad_al
            elif letra == "U":
                adicional = ad_u
            else:
                adicional = ad_mz

            punto = tratamiento.icd10.find(".")#Guarda la posicion del punto
            numpunto = int(tratamiento.icd10[punto + 1:])#Guarda el numero despues del punto
            monto = tratamiento.montobase + fijo + adicional#Base+fijo+adicional(depende de la letra)
            porcentaje = round(tratamiento.montobase * numpunto / 100,2)#Saca el porcentaje y lo redondea en dos numeros despues de la coma
            monto_final = monto + porcentaje
            montos_finales.append(monto_final)

    print()
    return montos_finales



def monto_fijo(tratamientos):
    n = len(tratamientos)

    for i in range(n):
        tratamiento = tratamientos[i]

        bloque = tratamiento.icd10[1:2]

        if "A" <= tratamiento.icd10 <= "L":
            monto_fijo = 20000

        elif "M" <= tratamiento.icd10 <= "P":
            monto_fijo = 15000 + 5000 * bloque

        else:
            monto_fijo = tratamiento.montobase * 0.10

        return monto_fijo

def calculo1(tratamientos):
    n = len(tratamientos)
    suma_fija = 0
    porcentaje_extra = 0

    for i in range(n):
        tratamiento = tratamientos[i]

        letra = tratamiento.icd10[0]

        if tratamientos.montobase > 60000:
            porcentaje_extra = porcentaje_normal(tratamiento)

            if tratamiento.complejidad == "A" and letra != "U":
                suma_fija = tratamiento.montobase / 2

        monto_final = tratamiento.montobase + porcentaje_extra + suma_fija

        return monto_final

def calculo2(tratamientos):
    n = len(tratamientos)

    for i in range(n):
        tratamiento = tratamientos[i]

        letra = tratamiento.icd10[0]
        punto = tratamiento.icd10.find(".")

        if "A" <= letra <= "P":
            porcentaje_extra = porcentaje_normal(tratamiento)

        elif "Q" <= letra <= "Z":
            if tratamiento.complejidad == "A":
                porcentaje_extra = (int(tratamiento.icd10[punto + 1:]) * 2) / 100

            elif tratamientos.complejidad == "R":
                porcentaje_extra = tratamiento.montobase * 0.15

        monto_final = tratamiento.montobase + porcentaje_extra

        return monto_final

def calculo3(tratamientos):
    n = len(tratamientos)
    monto_extra = 0

    for i in range(n):
        tratamiento = tratamientos[i]

        if tratamiento.complejidad == "A":
            monto_extra = tratamiento.montobase * 0.30

        monto_extra = monto_fijo(tratamiento)

        if monto_extra > 60000:
            monto_extra = 60000

        monto_final = tratamiento.montobase + monto_extra

    return monto_final

def mostrar_quinto(tratamientos):
    n = len(tratamientos)
    cta = 0

    for i in range(n):

        tratamiento = tratamientos[i]

        if tratamiento.complejidad == "A":
            cta += 1

            if cta == 5:
                r1_2 = tratamiento.apellido
                return r1_2

    if cta < 5:
        print('No hay suficientes tratamientos de alta complejidad.')

def proces_linea(linea: str):
    data = []
    palabra = ""
    for ch in linea:
        if ch == "," or ch == "\n":
            data.append(
                palabra
            )
            palabra = ""
        else:
            palabra += ch
    return data

def cargar_tratamientos():
    tratamientos = []
    r1_1 = 0 #Contador de tratamientos
    with open("tratamientos.csv", "r", encoding="utf-8") as f:
        f.readline()
        for linea in f.readlines():
            data = proces_linea(linea)
            r1_1 += 1
            tratamientos.append(
                Tratamiento(
                    dni=data[0],
                    nombre=data[1],
                    apellido=data[2],
                    icd10=data[3],
                    montobase=data[4],
                    complejidad=data[5],
                    idalgoritmo=data[6],
                )
            )

    return tratamientos, r1_1

if __name__ == "__main__":#Seccion de prueba
    tratamientos, r1_1 = cargar_tratamientos()

    r1_2 = mostrar_quinto(tratamientos)
    print('r1.1: ', r1_1)
    print('r1.2: ', r1_2)