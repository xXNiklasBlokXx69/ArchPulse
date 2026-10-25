from src.memory import print_meminfo
from src.cpu import print_cpu_usage
from src.disk import print_disk_usage

if __name__== "__main__":
    # Your main code logic here
    print("ArchPulse - System Health")
    print("-------------------------")
    print_cpu_usage()
    print_meminfo()
    print_disk_usage()