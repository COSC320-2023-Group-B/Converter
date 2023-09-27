# CSV_conversion_GUI
This application converts the CSV files that the Caretaker device generates into reformatted CSV files that LabChart can read.

## Installation
To create an executable file with no dependencies, use pyinstaller and access the dist/labchart_converter directory. e.g.
- `pip install pyinstaller`
- `pyinstaller labchart_converter.py`
- `./dist/labchart_converter/labchart_converter`

Alternatively, install Python3 or later and access labchart_converter.py/. e.g.
- `sudo apt-get install python3.8 python3-pip`
- `python3 labchart_converter.py`



## Usage
- After recording medical data with the Caretaker wearable device and tablet, connect the tablet to a PC via the white USB cable.
- The tablet will appear as a USB drive. Navigate to the Caretaker folder and copy the CSV files to the desired location on the PC.
- Open the CSV_conversion_GUI application and select the CSV files to convert and the destination file path.