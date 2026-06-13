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


def primer_no_cubierto(actual, conjuntos):
   
    for b in conjuntos:
        if len(actual & b) == 0:
            return b
    return None


def backtrack(actual, conjuntos, mejor):
    # explora recursivamente, guardando la mejor solucion

    # poda: si ya superamos o igualamos la mejor solucion, cortar
    if len(actual) >= mejor["tam"]:
        return

    b = primer_no_cubierto(actual, conjuntos)

    if b is None:
       
        mejor["tam"] = len(actual)
        mejor["solucion"] = set(actual)
        return

    for elem in b:
        if elem in actual:
            continue
        backtrack(actual | {elem}, conjuntos, mejor)


def hitting_set_backtracking(n, conjuntos):
    # cota superior inicial: n+1 
    mejor = {"tam": n + 1, "solucion": None}

    backtrack(frozenset(), conjuntos, mejor)

    return mejor["tam"], mejor["solucion"]


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tp3.py ruta/a/listado.txt")
        sys.exit(1)

    path = sys.argv[1]
    n, m, conjuntos, nombres = leer_instancia(path)

    inicio = time.perf_counter()
    tam, solucion = hitting_set_backtracking(n, conjuntos)
    fin = time.perf_counter()

    jugadores_solucion = sorted(nombres[i] for i in solucion)

    print(f"n = {n}, m = {m}")
    print(f"Tamanio del Hitting-Set optimo: {tam}")
    print(f"Hitting-Set: {jugadores_solucion}")
    print(f"Tiempo de ejecucion: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main()