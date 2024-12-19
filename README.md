# Game Hardware Checker

Game Hardware Checker is a Python application that helps users determine whether their computer's hardware meets the requirements for popular games. It calculates estimated FPS based on the hardware's benchmarks compared to game requirements.

## Features

- Detects your system's CPU, GPU, and RAM automatically.
- Verifies detected hardware against a local database of benchmarks.
- Allows users to add new hardware and games to the database.
- Estimates FPS for selected games based on your hardware.

---

## Installation

Follow these steps to set up and run the project:

### Prerequisites

1. **Python**: Ensure you have Python 3.8 or later installed. You can download it from [python.org](https://www.python.org/downloads/).
2. **Pip**: Ensure `pip` is installed and updated:
   ```bash
   python -m pip install --upgrade pip
   pip install psutil gputil py-cpuinfo

