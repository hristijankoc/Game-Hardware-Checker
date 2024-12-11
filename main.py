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

# Let the user choose a game
def choose_game(game_data):
    print("\nAvailable Games:")
    for idx, game_name in enumerate(game_data.keys(), 1):
        print(f"{idx}. {game_name}")
    print(f"{len(game_data) + 1}. Add a new game")

    game_choice = int(input("\nChoose a game (number): "))
    if game_choice == len(game_data) + 1:
        return add_new_game(game_data)
    else:
        selected_game = list(game_data.keys())[game_choice - 1]
        return game_data[selected_game]

# Add a new game to the database
def add_new_game(game_data):
    game_name = input("Enter the name of the new game: ").strip()
    cpu_benchmark = int(input(f"Enter minimum CPU benchmark for '{game_name}': "))
    gpu_benchmark = int(input(f"Enter minimum GPU benchmark for '{game_name}': "))
    new_game = {
        "name": game_name,
        "cpu_benchmark": cpu_benchmark,
        "gpu_benchmark": gpu_benchmark,
    }

    save_game = input("Would you like to save this game to the database? (yes/no): ").strip().lower()
    if save_game in ["yes", "y"]:
        game_data[game_name] = new_game
        save_json(game_data, "game_data.json")
        print(f"'{game_name}' has been added to the database.")
    return new_game

# Calculate FPS based on hardware and game requirements
def calculate_fps(hardware, game, cpu_data, gpu_data):
    cpu_benchmark = cpu_data[hardware["cpu"]]["benchmark"]
    gpu_benchmark = gpu_data[hardware["gpu"]]["benchmark"]

    cpu_required = game["cpu_benchmark"]
    gpu_required = game["gpu_benchmark"]

    cpu_ratio = cpu_benchmark / cpu_required
    gpu_ratio = gpu_benchmark / gpu_required

    # Estimate FPS (baseline is 60 FPS for matching benchmarks)
    estimated_fps = 60 * min(cpu_ratio, gpu_ratio)
    return estimated_fps

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

    # Let the user choose a game
    selected_game = choose_game(game_data)
    print(f"\nYou selected: {selected_game['name']}")

    # Calculate FPS
    estimated_fps = calculate_fps(hardware, selected_game, cpu_data, gpu_data)
    print(f"\nEstimated FPS for {selected_game['name']}: {estimated_fps:.2f} FPS")
    if estimated_fps >= 30:
        print("You can play this game at a decent performance level.")
    elif 15 <= estimated_fps < 30:
        print("You can play this game, but performance may be poor.")
    else:
        print("Your hardware is not sufficient to play this game.")

if __name__ == "__main__":
    main()
