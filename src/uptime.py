def get_uptime():
    """
    Read system uptime and return it in seconds.
    """
    with open('/proc/uptime', 'r') as f:
        uptime_second = float(f.readline().split()[0])
    return uptime_second


def print_uptime():
    """
    Display system uptime in days, hours, and minutes.
    """
    uptime_second = int(get_uptime())
    #get days, hours, minutes using divmod
    days, remainder = divmod(uptime_second, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"System Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")