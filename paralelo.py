import sys
import threading

# paralelo.py — Hito 1
# Versión multi-hilo de la suma del vector.

# Primitiva de sincronización equivalente a std::mutex
mtx = threading.Lock()
proximo = 0

# Tamaño de bloque de trabajo
BLOQUE = 1 << 16

def worker(data, n, idx, parciales):
    global proximo
    acc = 0.0

    while True:
        # TODO Resuelto: Tomar un rango [lo, hi) de forma exclusiva
        with mtx:  # 1. lock_guard sobre `mtx`
            if proximo >= n:  # 2. si proximo >= n, no hay más trabajo
                break
            
            # 3. lo = proximo; avanzar proximo en BLOQUE
            lo = proximo
            proximo += BLOQUE
            
            # Asegurarse de no pasarse de 'n'
            if proximo > n:
                proximo = n
            
            hi = proximo

        # El ciclo de suma queda FUERA del candado para permitir paralelismo real
        acc += sum(data[lo:hi])

    # Cada hilo escribe en su propia entrada de parciales
    parciales[idx] = acc

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else (1 << 24)
    t = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    
    if n < 1 or t < 1:
        print("N >= 1 y T >= 1", file=sys.stderr)
        sys.exit(1)

    data = [1.0] * n
    parciales = [0.0] * t
    hilos = []

    global proximo
    proximo = 0

    for i in range(t):
        h = threading.Thread(target=worker, args=(data, n, i, parciales))
        hilos.append(h)
        h.start()

    for h in hilos:
        h.join()

    # Reducción serial de T parciales
    total = sum(parciales)

    print(f"N={n} T={t} suma={total}")

if __name__ == "__main__":
    main()