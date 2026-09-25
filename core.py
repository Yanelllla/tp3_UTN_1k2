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

def porcentaje_normal(Tratamiento):

    punto = Tratamiento.icd10.find(".")
    porcentaje_extra = int(Tratamiento.icd10[punto + 1:]) / 100

    return porcentaje_extra

#Falta terminar
def monto_fijo(Tratamiento):
    n = len(Tratamiento)

    for i in range(n):
        bloque = Tratamiento.icd10[i].find()
        if "A" <= Tratamiento.icd10[i] <= "L":
            monto_fijo = 20000

        elif "M" <= Tratamiento.icd10[i] <= "P":
            monto_fijo = 15000 + 5000

def calculo1(Tratamiento):
    n = len(Tratamiento)
    suma_fija = 0
    porcentaje_extra = 0

    for i in range(n):
        letra = Tratamiento.icd10[i][0]

        if Tratamiento.montobase[i] > 60000:
            porcentaje_extra = porcentaje_normal(Tratamiento)

            if Tratamiento.complejidad[i] == "A" and letra != "U":
                suma_fija = Tratamiento.montobase[i] / 2

        monto_final = Tratamiento.montobase[i] + porcentaje_extra + suma_fija

        return monto_final

def calculo2(Tratamiento):
    n = len(Tratamiento)

    for i in range(n):
        letra = Tratamiento.icd10[i][0]
        punto = Tratamiento.icd10[i].find(".")

        if "A" <= letra <= "P":
            porcentaje_extra = porcentaje_normal(Tratamiento)

        elif "Q" <= letra <= "Z":
            if Tratamiento.complejidad[i] == "A":
                porcentaje_extra = (int(Tratamiento.icd10[punto + 1:]) * 2) / 100

            elif Tratamiento.complejidad[i] == "R":
                porcentaje_extra = Tratamiento.montobase[i] * 0.15

        monto_final = Tratamiento.montobase[i] + porcentaje_extra

        return monto_final

def calculo3(Tratamiento):
    n = len(Tratamiento)
    monto_extra = 0

    for i in range(n):
        if Tratamiento.complejidad[i] == "A":
            monto_extra = Tratamiento.montobase[i] * 0.30


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
    ct = 0 #Contador de tratamientos
    with open("tratamientos.csv", "r", encoding="utf-8") as f:
        f.readline()
        for linea in f.readlines():
            data = proces_linea(linea)
            ct += 1
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

    return tratamientos, ct

if __name__ == "__main__":
    for i in cargar_tratamientos():
        print(str(i))