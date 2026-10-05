import core

def principal():

    op = -1
    while op != 0:
        print("1. Cargar tratamientos")
        print("2. Mostrar resultados")
        print("3. Salir(0)")
        print()
        op = int(input("Ingrese opción: "))

        if op == 1:
            tratamientos, r1_1 = core.cargar_tratamientos()
            core.calcular_monto_final(tratamientos)
            r1_2 = core.mostrar_quinto(tratamientos)

            print("r1.1:", r1_1)
            print("r1.2:", r1_2)
            print()

        if op == 2:
            r2_1 = core.diferencia_promedio(tratamientos)
            letra_mayor, may_cant = core.contar_letra(tratamientos)
            r2_4 = core.dni_mayor_monto(tratamientos)

            print("r2.1: ", r2_1)
            print("r2.2: ", letra_mayor)
            print("r2.3: ", may_cant)
            print("r2.4: ", r2_4)
            print()

if __name__ == '__main__':
    principal()