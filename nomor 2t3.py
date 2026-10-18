import multiprocessing as mp
import random
import time

def worker_queue(queue, num_samples):
    # Menjumlahkan 1 juta angka acak
    subtotal = sum(random.random() for _ in range(num_samples))
    queue.put(subtotal)

def run_queue_version():
    queue = mp.Queue()
    processes = []
    num_samples = 1_000_000
    
    start = time.time()
    for _ in range(4):
        p = mp.Process(target=worker_queue, args=(queue, num_samples))
        processes.append(p)
        p.start()

    total = 0
    for _ in range(4):
        total += queue.get()

    for p in processes:
        p.join()
        
    end = time.time()
    return end - start, total

if __name__ == '__main__':
    t_queue, res_q = run_queue_version()
    print(f"[Queue / Message Passing] Waktu: {t_queue:.4f} detik | Total: {res_q:.2f}")