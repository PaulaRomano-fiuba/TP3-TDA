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


def resolver_pl(n, conjuntos, nombres):

    modelo = LpProblem("SetCover", LpMinimize)

    # Variables binarias
    x = LpVariable.dicts("x", range(n), cat="Binary")

    # Función objetivo: minimizar cantidad de elementos elegidos
    modelo += lpSum(x[i] for i in range(n))

    # Restricciones: cada conjunto debe tener al menos un elemento elegido
    for i, conjunto in enumerate(conjuntos):
        modelo += lpSum(x[j] for j in conjunto) >= 1

    # Resolver
    modelo.solve(PULP_CBC_CMD(msg=False))

    solucion = [
        nombres[i]
        for i in range(n)
        if value(x[i]) > 0.5
    ]

    return solucion, value(modelo.objective)


def main():

    archivo = sys.argv[1]  # archivo de entrada

    n, m, conjuntos, nombres = leer_instancia(archivo)
    
    inicio = time.perf_counter()
    solucion, cantidad = resolver_pl(n, conjuntos, nombres)
    fin = time.perf_counter()

    solucion.sort()
    
    print(f"n = {n}, m = {m}")
    print(f"Tamanio del Hitting-Set optimo: {cantidad}")
    print(f"Hitting-Set: {solucion}")
    print(f"Tiempo de ejecucion: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main()