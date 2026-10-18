import multiprocessing as mp
import time

def producer(queue):
    for i in range(10):
        # Tugas CPU-bound: komputasi berat
        val = sum(j * j for j in range(500000))
        queue.put(val)
    queue.put(None)  # Sentinel/Sinyal Selesai

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        # Melakukan pengolahan CPU-bound
        _ = [item ** 0.5 for _ in range(100)]

if __name__ == '__main__':
    queue = mp.Queue()
    p1 = mp.Process(target=producer, args=(queue,))
    p2 = mp.Process(target=consumer, args=(queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()