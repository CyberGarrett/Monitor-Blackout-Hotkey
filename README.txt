I made this so I can focus when I game, read, or write, and minimize eye strain. Configurable for 1-n displays, each instance supports a single hotkey to toggle a configuration. Use multiple projects for multiple hotkeys, though I will try to integrate this in future updates.

For ease of use, be sure to create a shortcut to your .ahk file and add it to your start menu folder, that way the script will be live when you log in. 

Overview

This solution provides a way to toggle black screens on specified monitors using a hotkey. The solution consists of a Python script, a batch script, and an AutoHotkey script. When the hotkey is triggered, the Python script either creates black screens on the specified monitors or removes them if they are already present. Additionally, it adjusts the brightness of the specified monitors. This black screen on top of the darkened displays helps prevents snooping, wether from over the shoulder or inference from graphics processes. 

Packages Required


    Python 3.x
    PyQt5
    pywin32

Installation

    Install Python packages:

    sh

    pip install pyqt5 pywin32

    Download and extract the script files to a directory on your computer.

Configuration

Modify the config.ini file in the same directory as the script with the following format:

ini

[Settings]
brightness_levels = 0,100,0
default_brightness = 80,80,80
blackout_monitors = 0,1,1

    brightness_levels: A comma-separated list of brightness levels for each monitor when toggling on (0-100).
    default_brightness: A comma-separated list of default brightness levels for each monitor when toggling off (0-100).
    blackout_monitors: A comma-separated list of binary values (0 or 1) indicating which monitors to create blackout screens on (1 = blackout, 0 = no blackout).

Usage
Running the Script

To test the script, double click the .bat file after verifying correct config values and file paths in both the .ini and .bat files.

Script Functionality

    The script will read the configuration file (config.ini) to get the specified brightness levels, default brightness levels, and blackout monitor settings.
    If the script is run for the first time, it will set the brightness to the specified levels and create blackout screens on the specified monitors.
    If the script is run again, it will switch the brightness to the default levels and remove the blackout screens.

Example

Given the following configuration:

ini

[Settings]
brightness_levels = 0,100,0
default_brightness = 80,80,80
blackout_monitors = 0,1,1

    Monitor 0 will have its brightness set to 0 and no blackout screen.
    Monitor 1 will have its brightness set to 100 and a blackout screen.
    Monitor 2 will have its brightness set to 0 and a blackout screen.
    When toggling off, all monitors will have their brightness set to 80 and blackout screens will be removed.

Troubleshooting

    Ensure that your monitors support DDC/CI commands. You can usually enable DDC/CI in the monitor's on-screen display (OSD) settings.
    Some cheap aftermarket display adapters (such as an HDMI to USB Display Adapter) may not support DDC/CI 

License

This project is licensed under the GNU GPL v3.0 License. 

