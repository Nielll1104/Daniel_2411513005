import time
import multiprocessing as mp
import matplotlib.pyplot as plt

# Fungsi pembantu untuk mengecek bilangan prima
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Fungsi worker untuk menghitung jumlah prima pada sebuah chunk (bagian data)
def hitung_prima_chunk(chunk):
    count = 0
    for n in chunk:
        if is_prime(n):
            count += 1
    return count

if __name__ == '__main__':
    LIMIT = 200000
    workers = [1, 2, 4, 8]
    times = []

    # Menggunakan context 'spawn' agar kompatibel di Windows (pengganti 'fork')
    ctx = mp.get_context('spawn')

    for w in workers:
        start = time.time()
        
        # Membagi rentang angka ke dalam beberapa chunk sejumlah worker
        data = range(1, LIMIT)
        chunk_size = len(data) // w
        chunks = [list(data[i:i + chunk_size]) for i in range(0, len(data), chunk_size)]
        
        # Eksekusi dengan Pool
        with ctx.Pool(processes=w) as pool:
            results = pool.map(hitung_prima_chunk, chunks)
            total_prima = sum(results)
        
        end = time.time()
        exec_time = end - start
        times.append(exec_time)
        print(f"Worker: {w}, Waktu: {exec_time:.4f} detik | Total Prima: {total_prima}")

    # Menghitung Speedup
    t1 = times[0]
    speedup_actual = [t1 / t for t in times]

    # Hukum Amdahl Teoritis (Asumsi p = 0.95 bagian paralel)
    p = 0.95
    amdahl = [1 / ((1 - p) + (p / w)) for w in workers]

    # Plotting Grafis
    plt.figure(figsize=(8, 5))
    plt.plot(workers, speedup_actual, 'o-', label='Speedup Aktual')
    plt.plot(workers, amdahl, 's--', label='Hukum Amdahl Teoritis (p=0.95)')
    plt.plot(workers, workers, 'k:', label='Speedup Ideal (Linear)')
    plt.xlabel('Jumlah Worker')
    plt.ylabel('Speedup')
    plt.title('Speedup vs Jumlah Worker')
    plt.legend()
    plt.grid(True)
    plt.show()