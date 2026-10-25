# ArchPulse

A lightweight command-line system health monitor for Linux, built with Python.

ArchPulse provides an overview of your system's CPU utilization, memory consumption, disk usage, and uptime directly from the terminal.

## Features

- **CPU Monitoring:** Measure CPU utilization over a one-second interval.
- **Memory Monitoring:** Display total, available, and estimated used RAM.
- **Disk Monitoring:** Show disk capacity, used space, available space, and utilization percentage.
- **System Uptime:** Display how long your system has been running.
- **Command-Line Interface:** Run individual diagnostics or a complete system scan.

## Requirements

- Linux with the `/proc` filesystem
- Python 3
- `psutil` Python package

ArchPulse is developed and tested primarily on Arch Linux.

## Installation

Clone the repository:

```bash
git clone https://github.com/xXNiklasBlokXx69/ArchPulse.git
cd ArchPulse
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run a complete system scan:

```bash
python main.py scan
```

Or simply:

```bash
python main.py
```

Run individual diagnostics:

```bash
python main.py cpu
python main.py memory
python main.py disk
python main.py uptime
```

Display available commands:

```bash
python main.py --help
```

## Example Output

```text
ArchPulse - System Health
-------------------------
CPU Usage: 5.33%
Total Memory: 30.50 GiB
Available Memory: 21.07 GiB
Used Memory: 9.43 GiB
Total Disk Space: 1832.33 GiB
Used Disk Space: 888.93 GiB
Free Disk Space: 850.26 GiB
Disk Utilization: 51.10%
System Uptime: 0 days, 2 hours, 6 minutes, 20 seconds
```

Actual values depend on the system.

## Running Tests

ArchPulse uses Python's built-in `unittest` framework.

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The initial monitoring components have 19 automated tests covering CPU, memory, disk, and uptime functionality.

## Project Structure

```text
ArchPulse/
├── src/
│   ├── cpu.py
│   ├── memory.py
│   ├── disk.py
│   └── uptime.py
├── tests/
│   ├── test_cpu.py
│   ├── test_memory.py
│   ├── test_disk.py
│   └── test_uptime.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Planned Improvements

- Improved diagnostic error handling
- Automated CLI tests
- JSON report exports
- Configurable system health warnings
- Failed systemd service detection

## About

ArchPulse is a personal learning project developed as part of the Boot.dev Backend Developer Path.

The goal is to gain practical experience with Python, Linux system interfaces, command-line applications, automated testing, and software design.