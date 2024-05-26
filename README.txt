Overview

This solution provides a way to toggle black screens on specified monitors using a hotkey. The solution consists of a Python script, a batch script, and an AutoHotkey script. When the hotkey is triggered, the Python script either creates black screens on the specified monitors or removes them if they are already present. Additionally, it adjusts the brightness of the specified monitors.
Files Included

This Python script allows you to control the brightness of your monitors and create blackout screens on specified monitors. The script toggles between specified brightness levels and default brightness levels while creating/removing blackout screens based on a configuration file.
Prerequisites

    Python 3.x
    PyQt5
    pywin32

Installation

    Install Python packages:

    sh

    pip install pyqt5 pywin32

    Download and extract the script files to a directory on your computer.

Configuration

Create a config.ini file in the same directory as the script with the following format:

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

To run the script, use the following command:

sh

python set_brightness.py

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

License

This project is licensed under the GNU GPL v3.0 License. 

This should cover everything needed to set up, configure, and run the script, along with providing some troubleshooting tips and license information.