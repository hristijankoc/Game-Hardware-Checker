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

# Save data to JSON files
def save_json(data, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")

# Verify hardware against the database
def verify_hardware(hardware, cpu_data, gpu_data):
    print(f"Detected CPU: {hardware['cpu']}")
    print(f"Detected GPU: {hardware['gpu']}")

    # Verify CPU
    if hardware["cpu"] not in cpu_data:
        print("\nYour CPU is not in our database. Please choose from the following:")
        for idx, cpu_name in enumerate(cpu_data.keys(), 1):
            print(f"{idx}. {cpu_name}")
        print(f"{len(cpu_data) + 1}. Add a new CPU")

        choice = int(input("\nEnter your choice: "))
        if choice == len(cpu_data) + 1:
            new_cpu = input("Enter the name of your CPU: ")
            benchmark = int(input(f"Enter the benchmark score for {new_cpu}: "))
            cpu_data[new_cpu] = {"benchmark": benchmark}
            save_json(cpu_data, "cpu_data.json")
            hardware["cpu"] = new_cpu
        else:
            hardware["cpu"] = list(cpu_data.keys())[choice - 1]

    # Verify GPU
    if hardware["gpu"] not in gpu_data:
        print("\nYour GPU is not in our database. Please choose from the following:")
        for idx, gpu_name in enumerate(gpu_data.keys(), 1):
            print(f"{idx}. {gpu_name}")
        print(f"{len(gpu_data) + 1}. Add a new GPU")

        choice = int(input("\nEnter your choice: "))
        if choice == len(gpu_data) + 1:
            new_gpu = input("Enter the name of your GPU: ")
            benchmark = int(input(f"Enter the benchmark score for {new_gpu}: "))
            gpu_data[new_gpu] = {"benchmark": benchmark}
            save_json(gpu_data, "gpu_data.json")
            hardware["gpu"] = new_gpu
        else:
            hardware["gpu"] = list(gpu_data.keys())[choice - 1]

    return hardware

def main():
    print("Welcome to the Game Benchmark Checker!")

    # Detect hardware
    hardware = detect_hardware()

    # Load JSON data
    cpu_data = load_json("cpu_data.json")
    gpu_data = load_json("gpu_data.json")
    game_data = load_json("game_data.json")

    # Verify hardware
    hardware = verify_hardware(hardware, cpu_data, gpu_data)
    print(f"\nFinalized Hardware: CPU = {hardware['cpu']}, GPU = {hardware['gpu']}, RAM = {hardware['ram']}GB")

    # Display loaded data
    print("\nLoaded CPU Data:", cpu_data)
    print("Loaded GPU Data:", gpu_data)
    print("Loaded Game Data:", game_data)

if __name__ == "__main__":
    main()
