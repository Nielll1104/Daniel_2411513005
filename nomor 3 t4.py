import asyncio
import random

async def producer(queue):
    # Item berupa tuple: (prioritas, id_item, data)
    # Angka prioritas lebih kecil = prioritas lebih tinggi
    items = [
        (3, 1, "Tugas Rendah A"),
        (1, 2, "Tugas Tinggi B"),
        (2, 3, "Tugas Sedang C"),
        (1, 4, "Tugas Tinggi D"),
        (3, 5, "Tugas Rendah E")
    ]
    
    for item in items:
        await queue.put(item)
        print(f"[Producer] Memasukkan: {item[2]} (Prioritas: {item[0]})")
        await asyncio.sleep(0.1)
    
    # Masukkan sinyal selesai (None) untuk consumer sejumlah consumer worker
    for _ in range(2):
        await queue.put((float('inf'), 0, None))

async def consumer(name, queue):
    while True:
        priority, id_item, data = await queue.get()
        if data is None:
            queue.task_done()
            break
        
        print(f"  [Consumer {name}] Memproses: {data} [Prioritas {priority}]")
        await asyncio.sleep(0.4) # Simulasi proses I/O
        queue.task_done()

async def main():
    queue = asyncio.PriorityQueue()
    
    # Menjalankan 1 producer dan 2 consumer
    prod = asyncio.create_task(producer(queue))
    cons1 = asyncio.create_task(consumer("1", queue))
    cons2 = asyncio.create_task(consumer("2", queue))
    
    await prod
    await queue.join()
    
    cons1.cancel()
    cons2.cancel()

if __name__ == '__main__':
    asyncio.run(main())