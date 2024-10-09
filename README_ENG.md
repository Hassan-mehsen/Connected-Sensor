# Embedded Project - SI1151

## Project Description:
This project aims to develop a light measurement interface using the SI1151 sensor. It includes a C API to interface the sensor with the ENIB environment and a Human-Machine Interface (HMI) developed in PyQt5.

## Prerequisites:

### For the C API:
- GCC compiler
- ENIB environment installed and configured (or STM32CubeIDE)
- A serial terminal emulator (minicom or gtkterm)

### For the PyQt5 HMI:
- Python 3.x
- pip (Python package manager)
- Other dependencies (see requirements.txt)
- An IDE such as PyCharm, VSCode, or any other IDE of your choice

## Installation and Usage

### C API:

1. **API Compilation (if you are using the ENIB environment on Linux):**
   - Navigate to the `.../Connected-Sensor` directory and open it in a terminal.
   - Compile the code using the Makefile: `make`
   - Run **ocd &**
   - Run **dbg main.elf** to open the debugger and launch the program.
   - To view the serial communication, open a terminal and type `minicom -D /dev/ttyACM0 -b 115200` or use `gtkterm`. 
     To install them, type: 
     (sudo apt install minicom) or (sudo apt install gtkterm)

   **API Compilation (if you are using STM32CubeIDE):**
   - Open the IDE.
   - Open the project from your directories.
   - Click the **Build & Debug** button.
   - To view the serial communication, find the corresponding COM port (usually COM3 or COM4).
   - Open **PuTTY** (or use Tera Term or minicom via WSL).
   - Select Serial as the connection type.
   - Enter the COM port (in the Serial line field), e.g., 'COM3'.
   - Set the baud rate.
   - Click Open to start the serial connection.

### PyQt5 HMI:
1. **Dependency Installation:**
   - Create and activate a virtual environment: 
     **python -m venv venv**
     **source venv/bin/activate**  # On Windows, use `venv\Scripts\activate`
   - Ensure Python 3.x is installed.
   - Install dependencies using the `requirements.txt` file: navigate to `~/Downloads/Connected-Sensor` and type 
     `pip install -r requirements.txt`

2. **Launching the HMI:**
   - Ensure the board is properly connected to the PC, the sensor is linked to the board via the I2C bus, and the program is running via the debugger or STM32CubeIDE.
   - Navigate to the directory: `...../Connected-Sensor/IHM`
   - Run the main Python script: **python3 main.py**

## Sensor and Project Overview:
For a detailed guide on the sensor and the project, please refer to the `Guide_Prise_en_Main.pdf` document located in the `documentation` folder.
A video demonstration of the project is also available in the `Video` directory (file `Demo.mp4`).

Note: Git does not natively support the MP4 format. The video file Demo.mp4 is included for reference but cannot be viewed directly from the repository. You will need to download the file to watch the demonstration. The video can be found in the Video directory.


## Gantt Chart:
The Gantt chart outlining the project schedule is available in the `gantt.pdf` file located in the `documentation` folder.
