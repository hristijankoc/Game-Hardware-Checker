import psutil
import GPUtil
from cpuinfo import get_cpu_info

# Detect user's hardware
def detect_hardware():
    raw_cpu_info = get_cpu_info()
    cpu_name = raw_cpu_info.get("brand_raw", "Unknown CPU")

    gpus = GPUtil.getGPUs()
    gpu_name = gpus[0].name if gpus else "Unknown GPU"

    ram_size = psutil.virtual_memory().total // (1024 ** 3)  # GB

    return {"cpu": cpu_name, "gpu": gpu_name, "ram": ram_size}

def main():
    print("Welcome to the Game Benchmark Checker!")
    hardware = detect_hardware()
    print(f"Detected Hardware: CPU = {hardware['cpu']}, GPU = {hardware['gpu']}, RAM = {hardware['ram']}GB")

if __name__ == "__main__":
    main()
