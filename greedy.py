from collections import defaultdict
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


def resolver_greedy(n, conjuntos, nombres):

    conjuntos_no_cubiertos = set(range(len(conjuntos)))

    solucion = []

    while conjuntos_no_cubiertos:

        frecuencia = defaultdict(int)

        for idx_conjunto in conjuntos_no_cubiertos:
            for jugador in conjuntos[idx_conjunto]:
                frecuencia[jugador] += 1

        mejor_jugador = max(
            frecuencia,
            key=frecuencia.get
        )

        solucion.append(nombres[mejor_jugador])

        cubiertos = {
            i
            for i in conjuntos_no_cubiertos
            if mejor_jugador in conjuntos[i]
        }

        conjuntos_no_cubiertos -= cubiertos

    return solucion


def main():

    archivo = sys.argv[1]

    n, m, conjuntos, nombres = leer_instancia(archivo)

    inicio = time.perf_counter()

    solucion = resolver_greedy(
        n,
        conjuntos,
        nombres
    )

    fin = time.perf_counter()

    solucion.sort()

    print(f"n = {n}, m = {m}")
    print(f"Tamanio del Hitting-Set obtenido: {len(solucion)}")
    print(f"Hitting-Set: {solucion}")
    print(f"Tiempo de ejecucion: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main()