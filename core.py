class Tratamiento:
    def __init__(self, dni, nombre, apellido, icd10, montobase, complejidad, idalgoritmo):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.icd10 = icd10
        self.montobase = montobase
        self.complejidad = complejidad
        self.idalgoritmo = idalgoritmo
        self.montos_finales = 0

    def __str__(self):
        r = "Tratamiento"
        r += f"|DNI:{self.dni:<8}"
        r += f"|Nombre:{self.nombre:<12}"
        r += f"|Apellido:{self.apellido:<12}"
        r += f"|ICD10:{self.icd10:<8}"
        r += f"|Monto Base:{self.montobase:<8}"
        r += f"|Complejidad:{self.complejidad:<4}"
        r += f"|Id algoritmo:{self.idalgoritmo:<4}"
        r += f"|Monto Final:{self.montos_finales:<10}"
        return r


class Coberturas:
    def __init__(self, dni, codigo_obra_social, nivel_cobertura, tope_atencion):
        self.dni = dni
        self.codigo_obra_social = codigo_obra_social
        self.nivel_cobertura = nivel_cobertura
        self.tope_atencion = tope_atencion

    def __str__(self) -> str:
        r = "Cobertura"
        r += f"|DNI:{self.dni:<8}"
        r += f"|Codigo de Obra Social:{self.codigo_obra_social:<8}"
        r += f"|Nivel de Cobertura:{self.nivel_cobertura:<8}"
        r += f"|Tope de Atencion:{self.tope_atencion:<8}"
        return r

def calculonormal(tratamiento: Tratamiento):
    ad_al = 25000
    ad_mz = 40000
    ad_u = 100000
    fijo = 25000#Monto fijo establecido en el tp1


    letra = tratamiento.icd10[0]
    if "A" <= letra <= "L":
        adicional = ad_al
    elif letra == "U":
        adicional = ad_u
    else:
        adicional = ad_mz

    punto = tratamiento.icd10.find(".")#Guarda la posicion del punto

    numpunto = int(tratamiento.icd10[punto + 1:])#Guarda el numero despues del punto

    monto = float(tratamiento.montobase) + fijo + adicional #Base+fijo+adicional(depende de la letra)

    porcentaje = round((monto * numpunto / 100),2)#Saca el porcentaje y lo redondea en dos numeros despues de la coma

    tratamiento.montos_finales = monto + porcentaje

    return porcentaje

def monto_fijo(tratamiento: Tratamiento):

    punto = tratamiento.icd10.find(".")
    bloque = int(tratamiento.icd10[punto + 1:])
    letra = tratamiento.icd10[0]

    if "A" <= letra <= "L":
        monto_fijo = 20000

    elif "M" <= letra <= "P":
        monto_fijo = 15000 + 5000 * int(bloque)

    elif "Q" <= letra <= "Z":
        monto_fijo = tratamiento.montobase * 0.10

    return monto_fijo

def calculo1(tratamiento: Tratamiento):
    suma_fija = 0
    porcentaje_extra = 0

    letra = tratamiento.icd10[0]

    if tratamiento.montobase > 60000:
        porcentaje_extra = calculonormal(tratamiento)

        if tratamiento.complejidad == "A" and letra != "U":
            suma_fija = tratamiento.montobase / 2

    tratamiento.montos_finales = tratamiento.montobase + porcentaje_extra + suma_fija

def calculo2(tratamiento: Tratamiento):

    letra = tratamiento.icd10[0]
    punto = tratamiento.icd10.find(".")

    if "A" <= letra <= "P":
        porcentaje_extra = calculonormal(tratamiento)

    elif "Q" <= letra <= "Z":
        if tratamiento.complejidad == "A":
            porcentaje_extra = (float(tratamiento.montobase) * int(tratamiento.icd10[punto + 1:]) * 2 / 100)

        elif tratamiento.complejidad == "R":
            porcentaje_extra = tratamiento.montobase * 0.15

    tratamiento.montos_finales = tratamiento.montobase + porcentaje_extra

def calculo3(tratamiento: Tratamiento):

    if tratamiento.complejidad == "A":
        monto_extra = tratamiento.montobase * 0.30
        monto_extra += monto_fijo(tratamiento)

    else:# PARA QUE LA CONDICION ANTERIOR SEA VALIDA SE TIENE QUE PONER UN IF O ELIF PARA QUE NO SOBRE ESCRIBA EL VALOR DE ESTA VARIABLE
        monto_extra = monto_fijo(tratamiento)

    if monto_extra > 60000:
        monto_extra = 60000

    tratamiento.montos_finales = tratamiento.montobase + monto_extra

def calcular_monto_final(tratamientos: list[Tratamiento]):

    for tratamiento in tratamientos:

        if tratamiento.idalgoritmo == 1:
            calculo1(tratamiento)

        elif tratamiento.idalgoritmo == 2:
            calculo2(tratamiento)

        elif tratamiento.idalgoritmo == 3:
            calculo3(tratamiento)

        else:
            calculonormal(tratamiento)

def mostrar_quinto(tratamientos):
    cta = 0

    for tratamiento in tratamientos:
        if tratamiento.complejidad == "A":
            cta += 1

            if cta == 5:
                r1_2 = tratamiento.apellido
                return r1_2

    if cta < 5:
        print('No hay suficientes tratamientos de alta complejidad.')


def diferencia_promedio(tratamientos: list[Tratamiento]):
    acum = 0

    for tratamiento in tratamientos:
        resta = tratamiento.montos_finales - float(tratamiento.montobase)
        acum += resta

    prom = round((acum / len(tratamientos)), 2)

    print()
    return prom

def contar_letra(tratamientos):
    letras = 26 * [0]
    abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for tratamiento in tratamientos:

        letra = tratamiento.icd10[0]
        ind = abecedario.find(letra)

        letras[ind] += 1

    may_cant = letras[0]
    posicion = 0

    for k in range(26):
        if letras[k] > may_cant:
            may_cant = letras[k]
            posicion = k

    letra_mayor = abecedario[posicion]

    return letra_mayor, may_cant

def dni_mayor_monto(tratamientos):
    mayor_monto_final = 0

    for tratamiento in tratamientos:
        if tratamiento.complejidad == "A":
            if tratamiento.montos_finales > mayor_monto_final:
                mayor_monto_final = tratamiento.montos_finales
                r2_4 = tratamiento.dni

    return r2_4

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


def insert_in_order_dni(c: Coberturas, v:list[Coberturas]):# BULLSHIT
    n = len(v)
    i,d = 0, n - 1
    idx = "Nigga" #TODO: cambien esto XD
    while i <= d:
        p = (i + d) // 2
        c_p = v[p]
        if c_p.dni == c.dni:
            idx = c
            break
        if c_p.dni > c.dni:
            i += p + 1
        else:
            d += p - 1
    if i > d:
        idx = i
    v[idx:idx] = [c]

def load_coberturas() -> list[Coberturas]:
    coberturas = []
    f = open("coberturas.csv", "r", encoding="utf-8")
    f.readline()
    for line in f.readlines():
        data = proces_linea(line)
        insert_in_order_dni(
            Coberturas(
                dni=data[0],
                codigo_obra_social=data[1],
                nivel_cobertura=data[2],
                tope_atencion=data[3]
            ),
            coberturas
        )

    return coberturas


def load_tratamientos() -> list[Tratamiento]:
    tratamientos = []
    f = open("tratamientos.csv", "r", encoding="utf-8")
    f.readline()
    for linea in f.readlines():
        data = proces_linea(linea)
        tratamientos.append(
            Tratamiento(
                dni=data[0],
                nombre=data[1],
                apellido=data[2],
                icd10=data[3],
                montobase=float(data[4]),
                complejidad=data[5],
                idalgoritmo=int(data[6]),
            )
        )

    return tratamientos
