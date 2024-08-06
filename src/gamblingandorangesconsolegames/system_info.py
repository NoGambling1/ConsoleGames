import platform
import psutil
import datetime
import os

def get_system_info():
    info = {
        "OS": f"{platform.system()} {platform.release()}",
        "PY version": platform.python_version(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "node": platform.node(),
        "platform": platform.platform(),
        "system": platform.system(),
        "CPU cores": psutil.cpu_count(),
        "CPU usage": f"{psutil.cpu_percent()}%",
        "total RAM": f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB",
        "available RAM": f"{round(psutil.virtual_memory().available / (1024.0 **3), 2)} GB",
        "RAM usage": f"{psutil.virtual_memory().percent}%",
        "disk usage": f"{psutil.disk_usage('/').percent}%",
        "current directory": os.getcwd(),
        "current date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "current time": datetime.datetime.now().strftime("%H:%M:%S"),
    }
    return info

def display_system_info():
    info = get_system_info()
    print("SYSTEM INFORMATION:")
    for key, value in info.items():
        print(f"{key}: {value}")