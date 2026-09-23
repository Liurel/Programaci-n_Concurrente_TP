# Programación_Concurrente_TP

# Hito 1 — Concurrencia en CPU (Versión Python)

**Objetivo:** demostrar dominio de hilos y sincronización.

## ⚠️ Nota Importante sobre Python y el GIL (Global Interpreter Lock)

A diferencia de C++, implementar múltiples hilos (`threads`) en Python para tareas intensivas de CPU (como sumar millones de números) **no resultará en una mejora de rendimiento o *speedup***.

Esto se debe a una característica interna de Python llamada **GIL (Global Interpreter Lock)**. El GIL actúa como un semáforo que permite que **solo un hilo ejecute instrucciones de código Python a la vez**, sin importar cuántos núcleos tenga el procesador de tu computadora.
Por lo tanto, aunque la lógica del código sea concurrente y los hilos despachen bloques de memoria usando un `Lock` (cumpliendo con los requisitos de sincronización del trabajo), en la práctica se ejecutarán de forma secuencial intercalada. Es muy probable que al correr el `benchmark.py`, los tiempos con múltiples hilos sean iguales o incluso peores que la versión secuencial debido a la sobrecarga (*overhead*) de crear y cambiar entre hilos. **Deberás mencionar y analizar este fenómeno en tu informe al comparar tus mediciones con la aceleración teórica de la Ley de Amdahl.**

## Enunciado

1. Problema con paralelismo de **datos** claro. Este proyecto usa **suma de un vector grande** de flotantes.


2. Versión **secuencial** (`secuencial.py`) y versión **multi-hilo** (`paralelo.py`).


3. Uso de al menos **una** primitiva de sincronización (en este caso, `threading.Lock` para reemplazar el comportamiento del `std::mutex`).


4. Medir aceleración S(T) = T_seq / T(T) vs. número de hilos y comparar con la Ley de Amdahl, con una fracción secuencial declarada.



## Entregable

* Código que **ejecuta correctamente**

* Informe de 1–2 páginas: curva medida vs. teórica y **por qué** difieren (Aquí es donde debes explicar el impacto del GIL de Python mencionado arriba).


* Tabla de tiempos (mediana de ≥ 3 corridas)



## Ejecución

Asegúrate de estar posicionado en la misma carpeta donde guardaste los archivos `.py` y ejecuta los siguientes comandos desde tu terminal o consola:

```bash
python secuencial.py 16777216
python paralelo.py 16777216 4
python benchmark.py 16777216

```

*(Nota: 16777216 representa el valor de N, es decir, el tamaño del vector. El 4 representa la cantidad de hilos).*

## Criterio de “listo”

* [ ] `secuencial` y `paralelo` dan la misma suma (tolerancia float; con vector de unos, el total esperado es N).


* [ ] `paralelo` usa una primitiva de sincronización **real** (`Lock`) para la asignación dinámica de los bloques de trabajo.


* [ ] `benchmark` imprime T(T) y S(T) para varios T.


* [ ] informe con Amdahl y análisis (memoria, GIL de Python, sobre-suscripción, fracción secuencial, tamaño de bloque, …).
