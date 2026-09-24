import sys
import time
import threading
import statistics
import multiprocessing

# benchmark.py — Hito 1
# Mide tiempo de la versión secuencial y de la paralela al variar T,
# e imprime speedup S(T) = T_seq / T_par(T).

mtx = threading.Lock()
proximo = 0
BLOQUE = 1 << 16

def suma_secuencial(data, n):
    return sum(data[:n])

def worker(data, n, idx, parciales):
    global proximo
    acc = 0.0
    while True:
        with mtx:
            if proximo >= n:
                break
            lo = proximo
            proximo += BLOQUE
            if proximo > n:
                proximo = n
            hi = proximo
        acc += sum(data[lo:hi])
    parciales[idx] = acc

def suma_par(data, n, t):
    global proximo
    proximo = 0
    parciales = [0.0] * t
    hilos = []
    
    for i in range(t):
        h = threading.Thread(target=worker, args=(data, n, i, parciales))
        hilos.append(h)
        h.start()
        
    for h in hilos:
        h.join()
        
    return sum(parciales)

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else (1 << 24)
    if n < 1:
        print("N >= 1", file=sys.stderr)
        sys.exit(1)

    # Detectamos la cantidad de núcleos de la CPU
    hw = multiprocessing.cpu_count()
    data = [1.0] * n

    # TODO Resuelto: Mediana de >= 3 corridas
    corridas = 3
    tiempos_seq = []
    s_seq = 0.0

    for _ in range(corridas):
        t0 = time.perf_counter()
        s_seq = suma_secuencial(data, n)
        t1 = time.perf_counter()
        tiempos_seq.append((t1 - t0) * 1000.0)

    ms_seq = statistics.median(tiempos_seq)

    print(f"hardware_concurrency={hw} N={n}")
    print("hilos,ms,speedup,suma")
    print(f"seq,{ms_seq:.2f},1.00,{s_seq}")

    candidatos = [1, 2, 4, 8, 16]
    for t in candidatos:
        if hw != 0 and t > hw * 2:
            continue  # Evita sobre-suscripción extrema en máquinas chicas
        
        tiempos_par = []
        s_par = 0.0
        
        for _ in range(corridas):
            u0 = time.perf_counter()
            s_par = suma_par(data, n, t)
            u1 = time.perf_counter()
            tiempos_par.append((u1 - u0) * 1000.0)
            
        ms_par = statistics.median(tiempos_par)
        speedup = (ms_seq / ms_par) if ms_par > 0.0 else 0.0
        
        print(f"{t},{ms_par:.2f},{speedup:.2f},{s_par}")

if __name__ == "__main__":
    main()