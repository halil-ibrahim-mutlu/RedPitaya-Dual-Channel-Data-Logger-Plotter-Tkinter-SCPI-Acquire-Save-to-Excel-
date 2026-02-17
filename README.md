# RedPitaya-Dual-Channel-Data-Logger-Plotter-Tkinter-SCPI-Acquire-Save-to-Excel-
# RedPitaya Dual-Channel Data Logger & Plotter (Tkinter + SCPI)

This project is a Python desktop GUI built with **Tkinter** that connects to a **Red Pitaya (SCPI over TCP socket)** (or a compatible SCPI device), acquires waveform data from **two channels**, saves the data to **Excel (.xlsx)**, plots the signals using **Matplotlib**, and also plots the **difference** between channel 1 and channel 2.

## Features
- ✅ Connects to device via TCP socket (SCPI)
- ✅ Acquire data from **Channel 1** (`ACQ:SOUR1:DATA?`)
- ✅ Acquire data from **Channel 2** (`ACQ:SOUR2:DATA?`)
- ✅ Save channel data to **Excel files**
- ✅ Plot signals inside the GUI (Matplotlib embedded in Tkinter)
- ✅ Display **mean line** on plots
- ✅ Compute and plot **difference (CH1 - CH2)**
- ✅ Save plots as **.jpg**
- ✅ Scrollable GUI layout (useful for multiple plots / buttons)

## How it works (High level)
1. The program opens a TCP connection to the device:
   - IP: `169.254.160.106`
   - Port: `5000`
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
pip install pandas matplotlib openpyxl
