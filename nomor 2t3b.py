import multiprocessing as mp
import random
import time

def worker_value(shared_val, lock, num_samples):
    # Menjumlahkan lokal dahulu agar meminimalkan lock-contention
    subtotal = sum(random.random() for _ in range(num_samples))
    with lock:
        shared_val.value += subtotal

def run_value_version():
    shared_val = mp.Value('d', 0.0) # 'd' untuk double precision float
    lock = mp.Lock()
    processes = []
    num_samples = 1_000_000

    start = time.time()
    for _ in range(4):
        p = mp.Process(target=worker_value, args=(shared_val, lock, num_samples))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
        
    end = time.time()
    return end - start, shared_val.value

if __name__ == '__main__':
    t_value, res_v = run_value_version()
    print(f"[Value / Shared Memory] Waktu: {t_value:.4f} detik | Total: {res_v:.2f}")