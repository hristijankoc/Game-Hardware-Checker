import json
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

# Load data from JSON files
def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Ensure the file exists.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON.")
        return {}

def main():
    print("Welcome to the Game Benchmark Checker!")

    # Detect hardware
    hardware = detect_hardware()
    print(f"Detected Hardware: CPU = {hardware['cpu']}, GPU = {hardware['gpu']}, RAM = {hardware['ram']}GB")

    # Load JSON data
    cpu_data = load_json("cpu_data.json")
    gpu_data = load_json("gpu_data.json")
    game_data = load_json("game_data.json")

    # Print loaded data
    print("\nLoaded CPU Data:", cpu_data)
    print("Loaded GPU Data:", gpu_data)
    print("Loaded Game Data:", game_data)

if __name__ == "__main__":
    main()
