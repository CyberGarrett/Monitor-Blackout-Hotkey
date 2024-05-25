import sys
import os
import configparser
import screen_brightness_control as sbc
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

class BlackScreen(QWidget):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.setGeometry(x, y, width, height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color: black;")
        self.show()

def set_brightness(levels, exclude_indices):
    monitors = sbc.list_monitors()
    for i, monitor in enumerate(monitors):
        if i not in exclude_indices:
            sbc.set_brightness(levels[i], display=monitor)

def create_black_screens(blackout_indices):
    app = QApplication(sys.argv)
    screens = []
    monitors = QApplication.screens()

    for i in blackout_indices:
        monitor = monitors[i]
        screen = BlackScreen(monitor.geometry().x(), monitor.geometry().y(), monitor.geometry().width(), monitor.geometry().height())
        screens.append(screen)

    return app, screens

def toggle_black_screens(config):
    temp_dir = os.getenv('TEMP')
    toggle_file = os.path.join(temp_dir, "black_screen_toggle")
    screens = []

    try:
        blackout_indices = list(map(int, config['Settings']['blackout_monitors'].split(',')))
        brightness_levels = list(map(int, config['Settings']['brightness_levels'].split(',')))
    except KeyError as e:
        print(f"Configuration error: Missing key {e}")
        return

    if os.path.exists(toggle_file):
        print("Removing black screens.")
        with open(toggle_file, "r") as f:
            pids = f.readlines()
        for pid in pids:
            try:
                os.kill(int(pid), 9)
            except:
                pass
        set_brightness([100] * len(brightness_levels), blackout_indices)  # Reset brightness to 100% for non-blackout monitors
        os.remove(toggle_file)
    else:
        print("Creating black screens.")
        app, screens = create_black_screens(blackout_indices)
        set_brightness(brightness_levels, blackout_indices)  # Set brightness levels as per config for blackout monitors
        with open(toggle_file, "w") as f:
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
        
    toggle_black_screens(config)
