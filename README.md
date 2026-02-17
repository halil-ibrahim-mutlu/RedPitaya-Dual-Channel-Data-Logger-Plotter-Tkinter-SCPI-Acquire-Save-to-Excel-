# RedPitaya-Dual-Channel-Data-Logger-Plotter-Tkinter-SCPI-Acquire-Save-to-Excel-

This project is a Python-based desktop application developed with Tkinter that interfaces with a Red Pitaya device via SCPI over TCP/IP. The application performs real-time dual-channel data acquisition, processes waveform data, exports measurements to Excel, and provides signal visualization and comparative analysis through embedded Matplotlib plots. It also includes channel difference calculation and automated plot export in JPEG format.

!!!   Pay attention ıp and port number generaly you can learn tehm on the carh ot web interface  for example redpitaya card prenset both way  
this code run like a client
server code code is in the redpitaya iy you wanna cahnge code pay attention fpga code sometimes you need to alter fpga codes also you can do it 

 !!!!!     ## Features
- ✅ Connects to device via TCP socket (SCPI)
- ✅ Acquire data from **Channel 1** (`ACQ:SOUR1:DATA?`)
- ✅ Acquire data from **Channel 2** (`ACQ:SOUR2:DATA?`)
- ✅ Save channel data to **Excel files**
- ✅ Plot signals inside the GUI (Matplotlib embedded in Tkinter)
- ✅ Display **mean line** on plots
- ✅ Compute and plot **difference (CH1 - CH2)**
- ✅ Save plots as **.jpg**
- ✅ Save datas in excel (excel created in codes otomatically )
- ✅ Scrollable GUI layout (useful for multiple plots / buttons)

## How it works (High level)
1. The program opens a TCP connection to the device:
   - IP: `your ip `
   - Port: `port number `
2. It starts acquisition and requests waveform data via SCPI.
3. Received data is parsed, converted to numeric values, and cleaned.
4. Channel data is exported to Excel.
5. Plots are shown in the GUI and can be saved as images.
6. The difference plot uses synchronized lengths of both channels.

## Requirements
- Python 3.x
- tkinter (usually included with Python on Windows/macOS)
- pandas
- matplotlib
- openpyxl (needed by pandas for writing `.xlsx`)

Install dependencies:
```bash
pip install pandas ma


tplotlib openpyxl
