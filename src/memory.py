def read_meminfo():
    """
    Reads /proc/meminfo and returns total and available memory in GiB.
    Raises ValueError if required memory information is missing or invalid.
    """
    meminfo = {}

    with open('/proc/meminfo', 'r') as f:
        for line in f:
            key, value = line.split(':', 1)
            key = key.strip()

            if key in ('MemTotal', 'MemAvailable'):
                meminfo[key] = int(value.split()[0]) / (1024**2)

    # Validate that both required values exist
    if 'MemTotal' not in meminfo or 'MemAvailable' not in meminfo:
        raise ValueError("Missing required memory information")

    total = meminfo['MemTotal']
    available = meminfo['MemAvailable']

    # Validate memory values
    if total <= 0:
        raise ValueError("Total memory must be greater than zero")

    if available < 0 or available > total:
        raise ValueError("Available memory must be between 0 and total memory")

    return total, available


def print_meminfo():
    """
    Prints total, available, and used memory in GiB.
    """
    total, available = read_meminfo()
    used = total - available

    print(f"Total Memory: {total:.2f} GiB")
    print(f"Available Memory: {available:.2f} GiB")
    print(f"Used Memory: {used:.2f} GiB")