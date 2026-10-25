from src.cpu import get_cpu_usage
from src.memory import read_meminfo
from src.disk import get_disk_usage
from src.uptime import get_uptime

import json

def collect_system_info():
    """
    Collect system information and return it as a dictionary.
    """
    cpu_usage = get_cpu_usage()
    total_memory, available_memory = read_meminfo()
    total_disk, used_disk, free_disk, disk_utilization = get_disk_usage()
    uptime_seconds = get_uptime()

    return {
        "cpu": {
            "usage_percent": round(cpu_usage, 2)
        },
        "memory": {
            "total_gib": round(total_memory, 2),
            "available_gib": round(available_memory,2),
            "used_gib": round(total_memory - available_memory, 2),
        },
        "disk": {
            "total_gib": round(total_disk, 2),
            "used_gib": round(used_disk, 2),
            "free_gib": round(free_disk, 2),
            "usage_percent": round(disk_utilization, 2)
        },
        "uptime": {
            "seconds": round(uptime_seconds, 2)
        }
    }

def save_report(data, filename):
    """
    Save the collected system information to a JSON file
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

