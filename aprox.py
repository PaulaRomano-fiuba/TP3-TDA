from pulp import *
import sys
import time


def leer_instancia(path):

    with open(path, "r") as f:
        lineas = [l.strip() for l in f if l.strip() != ""]

    nombre_a_indice = {}
    nombres = []
    conjuntos_nombres = []

    for linea in lineas:
        jugadores = [j.strip() for j in linea.split(",")]
        conjuntos_nombres.append(jugadores)

        for jugador in jugadores:
            if jugador not in nombre_a_indice:
                nombre_a_indice[jugador] = len(nombres)
                nombres.append(jugador)

    conjuntos = []
    for jugadores in conjuntos_nombres:
        conjuntos.append({nombre_a_indice[j] for j in jugadores})

    n = len(nombres)
    m = len(conjuntos)

    return n, m, conjuntos, nombres


def resolver_pl_relajado(n, conjuntos, nombres):

    modelo = LpProblem("HittingSetRelajado", LpMinimize)

    # Variables reales entre 0 y 1
    x = LpVariable.dicts(
        "x",
        range(n),
        lowBound=0,
        upBound=1,
        cat="Continuous"
    )

    # Función objetivo
    modelo += lpSum(x[i] for i in range(n))

    # Restricciones: cada conjunto debe estar cubierto
    for conjunto in conjuntos:
        modelo += lpSum(x[j] for j in conjunto) >= 1

    # Resolver relajación lineal
    modelo.solve(PULP_CBC_CMD(msg=False))

    # b = tamaño del conjunto más grande
    b = max(len(conjunto) for conjunto in conjuntos)

    umbral = 1 / b

    # Redondeo
    solucion = [
        nombres[i]
        for i in range(n)
        if value(x[i]) >= umbral
    ]

    # Valores fraccionales (opcional, para análisis)
    valores_relajados = {
        nombres[i]: value(x[i])
        for i in range(n)
    }

    return solucion, valores_relajados, b, umbral


def main():

    archivo = sys.argv[1]

    n, m, conjuntos, nombres = leer_instancia(archivo)

    inicio = time.perf_counter()

    solucion, valores_relajados, b, umbral = resolver_pl_relajado(
        n,
        conjuntos,
        nombres
    )

    fin = time.perf_counter()

    solucion.sort()

    print(f"n = {n}, m = {m}")
    print(f"b = {b}")
    print(f"Tamanio del Hitting-Set obtenido: {len(solucion)}")
    print(f"Hitting-Set: {solucion}")

    #print("\nValores de la solución relajada:")
    #for jugador in sorted(valores_relajados):
    #    print(f"{jugador}: {valores_relajados[jugador]:.6f}")

    print(f"\nTiempo de ejecucion: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main()