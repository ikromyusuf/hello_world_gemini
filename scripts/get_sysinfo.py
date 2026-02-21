import platform
import subprocess
import os
import shutil

def get_os():
    os_name = platform.system()
    if os_name == "Darwin":
        try:
            p_name = subprocess.check_output(["sw_vers", "-productName"]).decode().strip()
            p_version = subprocess.check_output(["sw_vers", "-productVersion"]).decode().strip()
            return f"{p_name} {p_version}"
        except:
            return f"macOS {platform.mac_ver()[0]}"
    elif os_name == "Linux":
        try:
            return subprocess.check_output(["lsb_release", "-ds"]).decode().strip().replace('"', '')
        except:
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            return line.split("=")[1].strip().replace('"', '')
            except:
                pass
            return f"Linux {platform.release()}"
    elif os_name == "Windows":
        return f"Windows {platform.version()} ({platform.release()})"
    return f"{os_name} {platform.release()}"

def get_cpu():
    os_name = platform.system()
    if os_name == "Darwin":
        try:
            return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        except:
            return platform.processor()
    elif os_name == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            pass
        return platform.processor()
    elif os_name == "Windows":
        try:
            return subprocess.check_output(["wmic", "cpu", "get", "name"]).decode().split('\n')[1].strip()
        except:
            return platform.processor()
    return platform.processor()

def get_ram():
    os_name = platform.system()
    if os_name == "Darwin":
        try:
            mem_bytes = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip())
            return f"{mem_bytes / (1024**3):.0f} GB"
        except:
            return "Unknown"
    elif os_name == "Linux":
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        mem_kb = int(line.split(":")[1].strip().split(" ")[0])
                        return f"{mem_kb / (1024**2):.0f} GB"
        except:
            pass
    elif os_name == "Windows":
        try:
            mem_bytes = int(subprocess.check_output(["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"]).decode().split('\n')[1].strip())
            return f"{mem_bytes / (1024**3):.0f} GB"
        except:
            pass
    return "Unknown"

def get_disk():
    try:
        total, used, free = shutil.disk_usage("/")
        return f"Total: {total // (1024**3)}Gi, Used: {used // (1024**3)}Gi, Avail: {free // (1024**3)}Gi"
    except:
        return "Unknown"

def get_gpu():
    os_name = platform.system()
    if os_name == "Darwin":
        try:
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode()
            for line in output.split('\n'):
                if "Chipset Model" in line:
                    return line.split(":")[1].strip()
        except:
            pass
    elif os_name == "Linux":
        try:
            output = subprocess.check_output(["lspci"]).decode()
            for line in output.split('\n'):
                if "VGA" in line or "3D" in line:
                    return line.split(":")[2].strip()
        except:
            pass
    elif os_name == "Windows":
        try:
            return subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "name"]).decode().split('\n')[1].strip()
        except:
            pass
    return "Unknown"

def get_python():
    return platform.python_version()

print(f"Software")
print(f"- OS: {get_os()}")
print(f"- Python Version: {get_python()}")

print(f"\nHardware")
print(f"- HDD/SSD: {get_disk()}")
print(f"- RAM: {get_ram()}")
print(f"- GPU: {get_gpu()}")
print(f"- CPU: {get_cpu()}")
