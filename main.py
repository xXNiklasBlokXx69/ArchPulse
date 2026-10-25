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
        return True
    except(OSError, ValueError, IndexError) as e:
        print(f"[ERROR] {name}: {e}", file=sys.stderr)
        return False

def try_save(args):
    try:
        data = collect_system_info()
        save_report(data, args.output)
        print(f"Report saved to {args.output}")
        return True
    except (OSError, ValueError, IndexError, TypeError) as e:
        print(f"[ERROR] Report: {e}", file=sys.stderr)
        return False

def main():
    args = parser.parse_args()
    print("ArchPulse - System Health")
    print("-------------------------")
    if args.command == "scan":
        results = []
        results.append(run_diagnostics("CPU Usage", print_cpu_usage))
        results.append(run_diagnostics("Memory Info", print_meminfo))
        results.append(run_diagnostics("Disk Usage", print_disk_usage))
        results.append(run_diagnostics("Uptime", print_uptime))
        return 0 if all(results) else 1
    elif args.command == "cpu":
        success = run_diagnostics("CPU Usage", print_cpu_usage)
        return 0 if success else 1
    elif args.command == "memory":
        success = run_diagnostics("Memory Info", print_meminfo)
        return 0 if success else 1
    elif args.command == "disk":
        success = run_diagnostics("Disk Usage", print_disk_usage)
        return 0 if success else 1
    elif args.command == "uptime":
        success = run_diagnostics("Uptime", print_uptime)
        return 0 if success else 1
    elif args.command == "report":
        success = try_save(args)
        return 0 if success else 1


if __name__== "__main__":
    sys.exit(main())