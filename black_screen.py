import os
import sys
import configparser
import ctypes
from ctypes import wintypes
import win32api
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

# Constants
PHYSICAL_MONITOR_DESCRIPTION_SIZE = 128
MC_CAPS_BRIGHTNESS = 0x00000002
MONITOR_DEFAULTTONEAREST = 2

class PHYSICAL_MONITOR(ctypes.Structure):
    _fields_ = [
        ("hPhysicalMonitor", wintypes.HANDLE),
        ("szPhysicalMonitorDescription", wintypes.WCHAR * PHYSICAL_MONITOR_DESCRIPTION_SIZE)
    ]

# Load DLLs
dxva2 = ctypes.WinDLL('dxva2')
user32 = ctypes.WinDLL('user32')

class BlackScreen(QWidget):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.setGeometry(x, y, width, height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color: black;")
        self.show()

def get_physical_monitors():
    """
    Get handles to physical monitors.
    """
    monitors = []
    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        num_monitors = ctypes.c_uint()
        dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hMonitor, ctypes.byref(num_monitors))
        physical_monitors = (PHYSICAL_MONITOR * num_monitors.value)()
        dxva2.GetPhysicalMonitorsFromHMONITOR(hMonitor, num_monitors.value, physical_monitors)
        monitors.extend(physical_monitors)
        return True

    monitor_enum_proc_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, wintypes.LPRECT, wintypes.LPARAM)
    monitor_enum_proc_func = monitor_enum_proc_type(monitor_enum_proc)

    user32.EnumDisplayMonitors(None, None, monitor_enum_proc_func, 0)
    return monitors

def set_brightness(monitor, brightness):
    """
    Sets the brightness for a single monitor.
    
    :param monitor: Physical monitor handle.
    :param brightness: Brightness level (0-100).
    """
    return dxva2.SetMonitorBrightness(monitor.hPhysicalMonitor, brightness)

def set_brightness_for_all_monitors(brightness_levels):
    """
    Sets the brightness for all connected monitors based on the provided brightness levels.
    
    :param brightness_levels: A list of brightness levels for each monitor.
    """
    try:
        monitors = get_physical_monitors()
        print(f"Detected physical monitors: {len(monitors)}")
        
        for i, monitor in enumerate(monitors):
            if i < len(brightness_levels):
                level = brightness_levels[i]
                print(f"Setting brightness of monitor {i} to {level}")
                # Ensure the brightness level is within a valid range (0-100)
                level = max(0, min(100, level))
                if not set_brightness(monitor, level):
                    print(f"Failed to set brightness for monitor {i}")
            else:
                print(f"No brightness level specified for monitor {i}")
    except Exception as e:
        print(f"Error setting brightness: {e}")

def create_black_screens(blackout_indices):
    app = QApplication(sys.argv)
    screens = []
    monitors = QApplication.screens()

    for i in blackout_indices:
        monitor = monitors[i]
        screen = BlackScreen(monitor.geometry().x(), monitor.geometry().y(), monitor.geometry().width(), monitor.geometry().height())
        screens.append(screen)

    return app, screens

def toggle_brightness_and_blackout(config):
    """
    Toggles the brightness and blackout screens based on the current state.
    If the script has already run, it sets the brightness to default levels and removes blackout screens.
    Otherwise, it sets the brightness to specified levels and creates blackout screens.
    """
    temp_dir = os.getenv('TEMP')
    toggle_file = os.path.join(temp_dir, "brightness_toggle_state")
    pid_file = os.path.join(temp_dir, "black_screen_pids")

    brightness_levels = list(map(int, config['Settings']['brightness_levels'].split(',')))
    default_brightness = list(map(int, config['Settings']['default_brightness'].split(',')))
    blackout_monitors = list(map(int, config['Settings']['blackout_monitors'].split(',')))

    if os.path.exists(toggle_file):
        print("Switching to default brightness levels and removing blackout screens.")
        set_brightness_for_all_monitors(default_brightness)

        if os.path.exists(pid_file):
            with open(pid_file, "r") as f:
                pids = f.readlines()
            for pid in pids:
                try:
                    os.kill(int(pid), 9)
                except Exception as e:
                    print(f"Error killing process {pid.strip()}: {e}")
            os.remove(pid_file)
        
        os.remove(toggle_file)
    else:
        print("Switching to specified brightness levels and creating blackout screens.")
        set_brightness_for_all_monitors(brightness_levels)
        blackout_indices = [i for i, val in enumerate(blackout_monitors) if val == 1]
        app, screens = create_black_screens(blackout_indices)
        with open(toggle_file, "w") as f:
            f.write("1")
        with open(pid_file, "w") as f:
            for screen in screens:
                f.write(str(os.getpid()) + "\n")
        app.exec()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    config_file_path = os.path.join(os.path.dirname(__file__), config_file)
    
    print(f"Looking for configuration file at: {config_file_path}")
    
    if not os.path.exists(config_file_path):
        print(f"Configuration file '{config_file_path}' not found.")
        sys.exit(1)
        
    config.read(config_file_path)
    if 'Settings' not in config:
        print("Configuration error: 'Settings' section missing.")
        sys.exit(1)
        
    toggle_brightness_and_blackout(config)
