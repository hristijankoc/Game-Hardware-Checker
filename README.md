# Game Hardware Checker

Game Hardware Checker is a Python application designed to help users check if their computer hardware meets the requirements for popular games. It provides estimated FPS based on the benchmarks of your CPU and GPU compared to the game's requirements.

---

## Features

- **Hardware Detection**:
  - Automatically detects your CPU, GPU, and RAM.
- **Hardware Database**:
  - Verifies your hardware against a local benchmark database.
  - Automatically adds missing hardware to the database for future use.
- **Game Database**:
  - Includes popular games with predefined minimum hardware requirements.
  - Allows users to add new games with their hardware requirements.
- **FPS Estimation**:
  - Calculates estimated FPS based on your hardware and the selected game.
- **User-Friendly Workflow**:
  - Offers intuitive prompts for game selection and adding new entries.

---

## Installation

Follow these steps to set up the project on your system:

### Prerequisites

1. **Python 3.8 or Later**:
   - Download from [python.org](https://www.python.org/downloads/).

2. **Pip**:
   - Ensure `pip` is installed and updated:
     ```bash
     python -m pip install --upgrade pip
     ```

3. **Optional: Virtual Environment**:
   - Create and activate a virtual environment:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```

### Dependencies

Install the required Python libraries:
```bash
pip install psutil gputil py-cpuinfo




