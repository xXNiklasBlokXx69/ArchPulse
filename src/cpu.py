import time


def read_cpu_times():
    """
    Reads /proc/stat 
    Read the first line 
    Extract the numerical values
    Return them as integers
    """
    with open('/proc/stat', 'r') as f:
        first_line = f.readline()
        values = first_line.split()[1:]

    return [int(value) for value in values] 

def calculate_cpu_usage(first, second):
    """
    Calculate CPU utilization percentage between two readings.
    """
    total_first = sum(first[:8])
    total_second = sum(second[:8])

    total_diff = total_second - total_first
    
    if total_diff <= 0:
        return 0.0
    
    idle_first = first[3] + first[4]
    idle_second = second[3] + second[4]

    idle_diff = idle_second - idle_first

    cpu_usage = (1 - idle_diff / total_diff) * 100

    return cpu_usage

def get_cpu_usage():
    """
    Measure CPU utilization over a one-second interval.
    """
    first = read_cpu_times()
    time.sleep(1)
    second = read_cpu_times()
    cpu_usage = calculate_cpu_usage(first, second)
    return cpu_usage

def print_cpu_usage():
    """
    Print the current CPU utilization percentage.
    """
    cpu_usage = get_cpu_usage()
    print(f"CPU Usage: {cpu_usage:.2f}%")