import sys
import time


def leer_instancia(archivo):
    with open(archivo, "r") as f:
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


def cubierto(conjunto, actual):
    for elem in conjunto:
        if elem in actual:
            return True
    return False


def primer_no_cubierto(actual, conjuntos):
    for conj in conjuntos:
        if not cubierto(conj, actual):
            return conj
    return None


def backtracking(actual, conjuntos, mejor_tam):
    # si ya superamos o igualamos la mejor solucion conocida, poda
    if len(actual) >= mejor_tam:
        return mejor_tam, None

    conj = primer_no_cubierto(actual, conjuntos)

    if conj is None:
        return len(actual), actual[:]

    mejor_solucion = None

    for elem in conj:
        actual.append(elem)
        tam, sol = backtracking(actual, conjuntos, mejor_tam)
        actual.pop()

        if sol is not None and tam < mejor_tam:
            mejor_tam = tam
            mejor_solucion = sol

    return mejor_tam, mejor_solucion


def hitting_set_backtracking(n, conjuntos):
    tam, solucion = backtracking([], conjuntos, n + 1)
    return tam, solucion


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tp3.py ruta/a/listado.txt")
        sys.exit(1)

    archivo = sys.argv[1]
    n, m, conjuntos, nombres = leer_instancia(archivo)

    inicio = time.perf_counter()
    tam, solucion = hitting_set_backtracking(n, conjuntos)
    fin = time.perf_counter()
    
    jugadores_solucion = []
    for i in solucion:
        jugadores_solucion.append(nombres[i]) 
    
    print(f"Cantidad minima: {tam} ({jugadores_solucion})")
    print(f"Tiempo de ejecucion: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main()