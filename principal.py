import core

def principal():

    tratamientos = [] #Default
    coberturas = []
    op = -1
    while op != 0:
        print("0. Salir")
        print("1. Cargar afiliados")
        print("2. Cargar tratamientos")
        print("3. Mostrar resultados")
        print()
        op = int(input("Ingrese opción: "))

        if op == 1:
            coberturas = core.load_coberturas()

        if op == 2:
            tratamientos = core.load_tratamientos()

        if op == 3:
            if coberturas and tratamientos:
                core.calcular_monto_final(tratamientos)
                core.cobertura(tratamientos, coberturas)
                r3_1, r3_2, r3_3, r3_4, r3_5, r3_6 = core.calcular_resultados(tratamientos, coberturas)

                print("r3.1:", round(r3_1, 2))
                print("r3.2:", round(r3_2, 2))
                print("r3.3:", r3_3)
                print("r3.4:", r3_4)
                print("r3.5:", r3_5)
                print("r3.6:", r3_6)
            else:
                print('Error')


if __name__ == '__main__':
    principal()