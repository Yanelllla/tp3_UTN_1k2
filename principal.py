from core import Tratamiento

def principal():

    op = -1
    while op != 0:
        print("1. Cargar tratamientos")
        print("2. Mostrar resultados")
        print("3. Salir(0)")
        op = int(input("Ingrese opción: "))

        if op == 1:
            print("r1.1, r1.2")

        if op == 2:
            print("r2.1, r2.2, r2.3, r2.4")


if __name__ == '__main__':
    principal()