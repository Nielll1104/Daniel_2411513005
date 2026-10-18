import asyncio
import time
import matplotlib.pyplot as plt

# 25 nama paket PyPI valid yang populer
daftar_paket_banyak = [
    "requests", "numpy", "pandas", "matplotlib", "scipy",
    "flask", "django", "fastapi", "sqlalchemy", "pydantic",
    "beautifulsoup4", "selenium", "pytest", "black", "flake8",
    "scikit-learn", "tensorflow", "torch", "transformers", "opencv-python",
    "pillow", "pygame", "streamlit", "gradio", "celery"
]

async def simulasi_download_paket(paket, semaphore):
    async with semaphore:
        # Simulasi latensi jaringan I/O (misal: fetch metadata PyPI)
        await asyncio.sleep(0.1)
        return f"Paket {paket} selesai"

async def jalankan_eksperimen(batas):
    semaphore = asyncio.Semaphore(batas)
    start_time = time.time()
    
    # Menjalankan tugas secara asinkron untuk semua paket
    tasks = [simulasi_download_paket(p, semaphore) for p in daftar_paket_banyak]
    await asyncio.gather(*tasks)
    
    end_time = time.time()
    return end_time - start_time

async def main():
    batas_list = [1, 3, 5, 10, 20]
    waktu_total = []

    for batas in batas_list:
        waktu = await jalankan_eksperimen(batas)
        waktu_total.append(waktu)
        print(f"BATAS_KONKURENSI = {batas:2d} | Waktu Total = {waktu:.4f} detik")

    # Plotting Waktu vs Batas Konkurensi
    plt.figure(figsize=(8, 5))
    plt.plot(batas_list, waktu_total, marker='o', linestyle='-', color='b')
    plt.title("Waktu Eksekusi vs Batas Konkurensi")
    plt.xlabel("Batas Konkurensi")
    plt.ylabel("Waktu Total (detik)")
    plt.grid(True)
    plt.show()

# Untuk menjalankan di Jupyter Notebook gunakan: await main()
if __name__ == '__main__':
    asyncio.run(main())