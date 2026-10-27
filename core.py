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
        self.monto_cubierto = 0
        self.monto_no_cubierto = 0
        self.tope_aplicado = False
        self.codigo_obra_social = 0

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

def buscar_cobertura(coberturas: list[Coberturas], dni: int):
    i = 0
    d = len(coberturas) - 1

    while i <= d:
        p = (i + d) // 2
        cobertura = coberturas[p]

        if cobertura.dni == dni:
            return cobertura
        elif dni < cobertura.dni:
            d = p - 1
        else:
            i = p + 1

    return None

def cobertura(tratamientos: list[Tratamiento], coberturas: list[Coberturas]):

    for tratamiento in tratamientos:
        afiliado = buscar_cobertura(coberturas, tratamiento.dni)

        if afiliado is None:
            tratamiento.monto_cubierto = 0
            tratamiento.monto_no_cubierto = tratamiento.montos_finales
            tratamiento.tope_aplicado = False
            tratamiento.codigo_obra_social = 0

        else:
            tratamiento.codigo_obra_social = afiliado.codigo_obra_social

            if afiliado.nivel_cobertura == 1:
                if tratamiento.complejidad == "R":
                    porcentaje = 0.50
                else:
                    porcentaje = 0.40

            elif afiliado.nivel_cobertura == 2:
                if tratamiento.complejidad == "R":
                    porcentaje = 0.70
                else:
                    porcentaje = 0.60

            else:
                if tratamiento.complejidad == "R":
                    porcentaje = 0.90
                else:
                    porcentaje = 0.80

            monto = round(tratamiento.montos_finales * porcentaje, 2)

            if monto > afiliado.tope_atencion:
                monto = afiliado.tope_atencion
                tratamiento.tope_aplicado = True

            else:
                tratamiento.tope_aplicado = False

            tratamiento.monto_cubierto = monto
            tratamiento.monto_no_cubierto = round(tratamiento.montos_finales - monto, 2)

def calcular_resultados(tratamientos: list[Tratamiento], coberturas: list[Coberturas]):

    total_cubierto = 0
    total_no_cubierto = 0
    cantidad_topes = 0
    cantidad_sin_cobertura = 0

    montos_obras_sociales = 21 * [0]

    mayor_no_cubierto = tratamientos[0].monto_no_cubierto
    dni_mayor_no_cubierto = tratamientos[0].dni

    for tratamiento in tratamientos:

        total_cubierto += tratamiento.monto_cubierto
        total_no_cubierto += tratamiento.monto_no_cubierto

        if tratamiento.tope_aplicado:
            cantidad_topes += 1

        if tratamiento.codigo_obra_social == 0:
            cantidad_sin_cobertura += 1
        else:
            codigo = tratamiento.codigo_obra_social
            montos_obras_sociales[codigo] += tratamiento.monto_cubierto

        # Usar > y no >= para conservar el primero en caso de empate
        if tratamiento.monto_no_cubierto > mayor_no_cubierto:
            mayor_no_cubierto = tratamiento.monto_no_cubierto
            dni_mayor_no_cubierto = tratamiento.dni

    # Buscar la obra social que cubrió el mayor monto.
    # En caso de empate, queda el código menor.
    mayor_cubierto = -1
    codigo_mayor = 1

    for codigo in range(1, 21):
        if montos_obras_sociales[codigo] > mayor_cubierto:
            mayor_cubierto = montos_obras_sociales[codigo]
            codigo_mayor = codigo

    return total_cubierto, total_no_cubierto, cantidad_topes, cantidad_sin_cobertura, codigo_mayor, dni_mayor_no_cubierto

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

def insert_in_order_dni(c, v):
    i = 0
    d = len(v) - 1

    while i <= d:
        p = (i + d) // 2

        if v[p].dni == c.dni:
            break
        elif v[p].dni > c.dni:
            d = p - 1
        else:
            i = p + 1

    if i <= d:
        pos = p
    else:
        pos = i

    v[pos:pos] = [c]

def load_coberturas() -> list[Coberturas]:
    coberturas = []
    f = open("coberturas.csv", "r", encoding="utf-8")
    f.readline()
    for linea in f.readlines():
        data = proces_linea(linea)
        insert_in_order_dni(
            Coberturas(
                dni=int(data[0]),
                codigo_obra_social=int(data[1]),
                nivel_cobertura=int(data[2]),
                tope_atencion=float(data[3])
            ),
            coberturas
        )
    f.close()
    return coberturas


def load_tratamientos() -> list[Tratamiento]:
    tratamientos = []
    f = open("tratamientos.csv", "r", encoding="utf-8")
    f.readline()
    for linea in f.readlines():
        data = proces_linea(linea)
        tratamientos.append(
            Tratamiento(
                dni=int(data[0]),
                nombre=data[1],
                apellido=data[2],
                icd10=data[3],
                montobase=float(data[4]),
                complejidad=data[5],
                idalgoritmo=int(data[6]),
            )
        )
    f.close()
    return tratamientos
