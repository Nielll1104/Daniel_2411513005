import asyncio
import time

# 1. Memakai asyncio.sleep() (Non-blocking / Cooperative)
async def coroutine_async_sleep():
    await asyncio.sleep(1)
    print("-> asyncio.sleep selesai (Non-blocking)")

# 2. Memakai time.sleep() (Blocking I/O/Standard)
async def coroutine_time_sleep():
    time.sleep(1)  # Memblokir seluruh Event Loop!
    print("-> time.sleep selesai (BLOCKING!)")

# 3. Operasi CPU-bound murni tanpa await (Blocking CPU)
async def coroutine_cpu_bound():
    # Menghitung faktorial/loop besar tanpa await
    _ = [i * i for i in range(10**7)]
    print("-> CPU-bound murni selesai (BLOCKING CPU!)")

# Coroutine pengukur untuk memantau kelancaran event loop
async def coroutine_pengukur():
    for i in range(5):
        print(f"[Pengukur] Berjalan normal ke-{i+1}")
        await asyncio.sleep(0.3)

async def main():
    print("--- Uji 1: Dengan asyncio.sleep ---")
    await asyncio.gather(coroutine_async_sleep(), coroutine_pengukur())

    print("\n--- Uji 2: Dengan time.sleep (Blocking) ---")
    await asyncio.gather(coroutine_time_sleep(), coroutine_pengukur())

    print("\n--- Uji 3: Dengan CPU-bound murni (Blocking) ---")
    await asyncio.gather(coroutine_cpu_bound(), coroutine_pengukur())

if __name__ == '__main__':
    asyncio.run(main())