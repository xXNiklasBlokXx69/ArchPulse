# ArchPulse

**ArchPulse** is a lightweight, command-line system health monitoring tool for Linux, written in Python.

It provides information about CPU usage, memory usage, disk utilization, and system uptime. ArchPulse also supports exporting system information to JSON files for further analysis or integration with other tools.

This project was developed as part of the [Boot.dev](https://www.boot.dev/) Personal Project.

## Features

- **CPU Monitoring** — Measure CPU utilization using `/proc/stat`.
- **Memory Monitoring** — Display total, available, and estimated used RAM using `/proc/meminfo`.
- **Disk Monitoring** — Display total, used, and free disk space alongside disk utilization.
- **System Uptime** — Display how long the Linux system has been running.
- **Command-Line Interface** — Run individual diagnostics or a complete system scan.
- **JSON Reports** — Export system measurements to a structured JSON file.
- **Error Handling** — Report errors without stopping other diagnostics during a complete scan.
- **Exit Codes** — Return meaningful process exit codes for scripting and automation.
- **Automated Tests** — 46 unit tests covering system monitoring, report generation, and CLI functionality.

## Requirements

- Linux operating system
- Python 3.10 or newer
- `psutil` Python package

ArchPulse reads Linux-specific system files and is not designed to run natively on Windows or macOS.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/xXNiklasBlokXx69/ArchPulse.git
cd ArchPulse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

Run ArchPulse from the project root directory.

### Complete System Scan

```bash
python main.py
```

Or explicitly:

```bash
python main.py scan
```

Both commands display CPU, memory, disk, and uptime information.

### Individual Diagnostics

**CPU Usage**

```bash
python main.py cpu
```

**Memory Usage**

```bash
python main.py memory
```

**Disk Usage**

```bash
python main.py disk
```

**System Uptime**

```bash
python main.py uptime
```

### Example Output

```text
ArchPulse - System Health
-------------------------
CPU Usage: 5.34%
Total Memory: 30.50 GiB
Available Memory: 18.66 GiB
Used Memory: 11.84 GiB
Total Disk Space: 1832.33 GiB
Used Disk Space: 888.94 GiB
Free Disk Space: 850.24 GiB
Disk Utilization: 51.10%
System Uptime: 0 days, 2 hours, 44 minutes, 38 seconds
```

*Values are illustrative and will vary depending on the system.*

## JSON Report Generation

ArchPulse supports exporting system information to a JSON file.

### Default Output

```bash
python main.py report
```

This creates a file named `system.json` in the current working directory.

### Custom Output Filename

```bash
python main.py report --output my_system.json
```

An existing file at the specified path will be overwritten.

### Example JSON Report

```json
{
    "cpu": {
        "usage_percent": 5.34
    },
    "memory": {
        "total_gib": 30.5,
        "available_gib": 18.66,
        "used_gib": 11.84
    },
    "disk": {
        "total_gib": 1832.33,
        "used_gib": 888.94,
        "free_gib": 850.24,
        "usage_percent": 51.1
    },
    "uptime": {
        "seconds": 9878.72
    }
}
```

### Validate the Report

You can validate and format the generated JSON using Python:

```bash
python -m json.tool system.json
```

The report can be consumed by other programs, scripts, or monitoring tools.

## Exit Codes and Error Handling

ArchPulse returns standard process exit codes.

| Exit Code | Description |
|---|---|
| `0` | Command executed successfully |
| `1` | A diagnostic or report operation failed |
| `2` | Invalid command-line arguments |

Check the exit code of the previous command:

```bash
python main.py scan
echo $?
```

During a complete system scan, ArchPulse attempts all four diagnostics even if one fails.

Errors are written to standard error (`stderr`).

Example:

```text
[ERROR] Report: [Errno 2] No such file or directory: '/invalid/path/report.json'
```

A failed report operation returns exit code `1`.

## Project Structure

```text
ArchPulse/
├── main.py
├── src/
│   ├── cpu.py
│   ├── memory.py
│   ├── disk.py
│   ├── uptime.py
│   └── report.py
├── tests/
│   ├── test_cli.py
│   ├── test_cpu.py
│   ├── test_memory.py
│   ├── test_disk.py
│   ├── test_uptime.py
│   └── test_report.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Main Components

| File | Responsibility |
|---|---|
| `main.py` | Argument parsing, command execution, and exit codes |
| `src/cpu.py` | CPU utilization measurement |
| `src/memory.py` | Memory information collection |
| `src/disk.py` | Disk usage measurement |
| `src/uptime.py` | System uptime measurement |
| `src/report.py` | Collecting and exporting JSON reports |

## Testing

ArchPulse uses Python's built-in `unittest` framework and `unittest.mock` for automated testing.

Run all tests from the project root:

```bash
python -m unittest discover -s tests -v
```

Run individual test modules:

```bash
python -m unittest discover -s tests -p "test_cpu.py" -v
python -m unittest discover -s tests -p "test_memory.py" -v
python -m unittest discover -s tests -p "test_disk.py" -v
python -m unittest discover -s tests -p "test_uptime.py" -v
python -m unittest discover -s tests -p "test_report.py" -v
python -m unittest discover -s tests -p "test_cli.py" -v
```

### Test Coverage

The current test suite contains **46 automated tests**, covering:

- CPU utilization calculations and edge cases
- Memory parsing and validation
- Disk usage and utilization
- Uptime parsing and formatting
- CLI commands and default behavior
- JSON report collection and file writing
- Diagnostic and report errors
- Successful and failed command exit codes
- Continued execution of diagnostics when one fails

Latest verified local test result:

```text
----------------------------------------------------------------------
Ran 46 tests in 0.016s

OK
```

## How It Works

### CPU Monitoring

ArchPulse reads CPU time statistics from `/proc/stat`.

It takes two measurements approximately one second apart and calculates CPU utilization based on the difference between total and idle CPU time.

### Memory Monitoring

Memory information is obtained from `/proc/meminfo`.

Used memory is estimated as:

```text
Used Memory = Total Memory - Available Memory
```

The available memory value accounts for memory that the Linux kernel estimates can be made available without significant swapping.

### Disk Monitoring

Disk information is collected using `psutil.disk_usage("/")`.

The measurement covers the filesystem containing the root directory (`/`), rather than summing all mounted storage devices.

### System Uptime

System uptime is obtained from `/proc/uptime`.

ArchPulse converts the uptime into days, hours, minutes, and seconds for terminal display.

### JSON Export

The reporting module collects information from the monitoring functions, organizes the results into nested dictionaries, and serializes them using Python's built-in `json` module.

Measurements are rounded for human-readable reporting.

## Limitations

- Only supports Linux systems.
- CPU utilization requires a short sampling interval.
- Disk monitoring currently measures only the root filesystem.
- JSON reports represent a single snapshot rather than historical monitoring data.
- ArchPulse is a command-line tool and does not currently provide a graphical interface or background monitoring service.

## Future Improvements

Potential improvements for future versions include:

- Configurable CPU sampling intervals
- Monitoring multiple mounted filesystems
- Configurable resource usage thresholds
- Historical metrics collection
- Continuous monitoring mode
- Additional Linux system diagnostics

These features are outside the scope of version 1.0.

## License

No license has been specified yet. See the repository for any future licensing information.

## Author

Developed by [xXNiklasBlokXx69](https://github.com/xXNiklasBlokXx69).

**Repository:** https://github.com/xXNiklasBlokXx69/ArchPulse