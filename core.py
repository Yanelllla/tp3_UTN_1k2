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

def calculo1(tratamientos):
    n = len(tratamientos)

    for i in range(n):
        letra = tratamientos.icd10[i][0]
        punto = tratamientos.icd10[i].find(".")
        suma_fija = 0
        porcentaje_extra = 0

        if tratamientos.montobase[i] > 60000:
            porcentaje_extra = int(tratamientos.icd10[punto + 1:]) / 100
            if tratamientos.complejidad[i] == "A" and letra != "U":
                suma_fija = tratamientos.montobase[i] / 2

        monto_final = tratamientos.montobase[i] + porcentaje_extra + suma_fija

    return monto_final

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