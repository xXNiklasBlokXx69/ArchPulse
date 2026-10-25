from src.memory import print_meminfo
from src.cpu import print_cpu_usage
from src.disk import print_disk_usage
from src.uptime import print_uptime

import argparse

parser = argparse.ArgumentParser(
    description="ArchPulse - System Health Monitor"
)

parser.add_argument(
    "command",
    nargs="?",
    default="scan",
    choices=["scan", "cpu", "memory", "disk", "uptime"],
    help="Select which system information to display"
)
def main():
    args = parser.parse_args()
    print("ArchPulse - System Health")
    print("-------------------------")
    if args.command == "scan":
        print_cpu_usage()
        print_meminfo()
        print_disk_usage()
        print_uptime()
    elif args.command == "cpu":
        print_cpu_usage()
    elif args.command == "memory":
        print_meminfo()
    elif args.command == "disk":
        print_disk_usage()
    elif args.command == "uptime":
        print_uptime()


if __name__== "__main__":
    main()