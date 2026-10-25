import psutil

def get_disk_usage():
    """
    Get total, used, and free disk space in GiB.
    """

    usage = psutil.disk_usage('/')

    total = usage.total / (1024 ** 3)
    used = usage.used / (1024 ** 3)
    free = usage.free / (1024 ** 3)
    disk_utilization = usage.percent
    return total, used, free, disk_utilization

def print_disk_usage():
    """
    Print disk usage information.
    """
    total, used, free, disk_utilization = get_disk_usage()
    print(f"Total Disk Space: {total:.2f} GiB")
    print(f"Used Disk Space: {used:.2f} GiB")
    print(f"Free Disk Space: {free:.2f} GiB")
    print(f"Disk Utilization: {disk_utilization:.2f}%")