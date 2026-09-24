import sys
import time

# secuencial.py — Hito 1
# Suma secuencial de una lista grande de floats.

def suma_secuencial(data, n):
    # Sumamos directamente. En Python 'sum' está optimizado en C.
    return sum(data[:n])

def main():
    # N por defecto: 2^24 (16 777 216)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else (1 << 24)
    if n < 1:
        print("N debe ser >= 1", file=sys.stderr)
        sys.exit(1)

    data = [1.0] * n

    t0 = time.perf_counter()
    suma = suma_secuencial(data, n)
    t1 = time.perf_counter()
    
    ms = (t1 - t0) * 1000.0

    print(f"N={n} suma={suma} tiempo_ms={ms:.2f}")

if __name__ == "__main__":
    main()