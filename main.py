import sys

from src.memory import print_meminfo
from src.cpu import print_cpu_usage
from src.disk import print_disk_usage
from src.uptime import print_uptime
from src.report import collect_system_info, save_report

import argparse

parser = argparse.ArgumentParser(
    description="ArchPulse - System Health Monitor"
)

parser.add_argument(
    "command",
    nargs="?",
    default="scan",
    choices=["scan", "cpu", "memory", "disk", "uptime", "report"],
    help="Select which system information to display"
)

parser.add_argument(
    "--output",
    default="system.json",
    help="Output filename for JSON reports"
)

def run_diagnostics(name, function):
    try:
        function()
    except(OSError, ValueError, IndexError) as e:
        print(f"[ERROR] {name}: {e}", file=sys.stderr)


def main():
    args = parser.parse_args()
    print("ArchPulse - System Health")
    print("-------------------------")
    if args.command == "scan":
        run_diagnostics("CPU Usage", print_cpu_usage)
        run_diagnostics("Memory Info", print_meminfo)
        run_diagnostics("Disk Usage", print_disk_usage)
        run_diagnostics("Uptime", print_uptime)
    elif args.command == "cpu":
        run_diagnostics("CPU Usage", print_cpu_usage)
    elif args.command == "memory":
        run_diagnostics("Memory Info", print_meminfo)
    elif args.command == "disk":
        run_diagnostics("Disk Usage", print_disk_usage)
    elif args.command == "uptime":
        run_diagnostics("Uptime", print_uptime)
    elif args.command == "report":
        data = collect_system_info()
        save_report(data, args.output)
        print(f"Report saved to {args.output}")


if __name__== "__main__":
    main()