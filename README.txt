Overview

This solution provides a way to toggle black screens on specified monitors using a hotkey. The solution consists of a Python script, a batch script, and an AutoHotkey script. When the hotkey is triggered, the Python script either creates black screens on the specified monitors or removes them if they are already present. Additionally, it adjusts the brightness of the specified monitors.
Files Included

    black_screen_G.py: The Python script that creates and toggles black screens.
    toggle_black_screen_G.bat: A batch script to run the Python script.
    black_screen_G.ahk: An AutoHotkey script to bind the toggle functionality to a hotkey.
    config.ini: Configuration file to specify monitor settings.

How It Works

    Python Script (black_screen_G.py):
        Reads configuration from config.ini.
        Creates black screens on the specified monitors.
        Sets the brightness levels for each monitor as specified in the config.
        Uses a temporary file to track the state of the black screens and toggle them.

    Batch Script (toggle_black_screen_G.bat):
        Executes the Python script to perform the toggle operation.

    AutoHotkey Script (black_screen_G.ahk):
        Binds the batch script to a hotkey (Ctrl + Alt + C) to trigger the toggle functionality.

Setup Instructions

    Install PyQt5 and screen-brightness-control:
    Ensure you have the required libraries installed. Run the following commands in your command prompt:

    cmd

    pip install PyQt5 screen-brightness-control

    Modify Paths:
    Update the paths in the batch script (toggle_black_screen_G.bat) and AutoHotkey script (black_screen_G.ahk) to point to the correct locations of your files.

    Configure Monitors:
    Edit the config.ini file to specify the number of monitors, which monitors to black out, and the brightness levels.

    Run AutoHotkey Script:
    Start the AutoHotkey script (black_screen_G.ahk). Use the hotkey (Ctrl + Alt + C) to toggle the black screens.

Configuration File (config.ini)

The config.ini file should be placed in the same directory as the black_screen_G.py script. The file allows you to specify the monitor settings:

Example config.ini:

ini

[Settings]
monitor_count = 3
blackout_monitors = 0,2
brightness_levels = 0,100,0

    monitor_count: The total number of monitors connected.
    blackout_monitors: Comma-separated indices of the monitors to black out.
    brightness_levels: Comma-separated brightness levels for each monitor (0 to 100).

Customization

For different monitor setups:

    Edit the config.ini file to change the monitor settings.
    Specify the monitors to black out and the brightness levels for each monitor.

Troubleshooting

    Ensure all paths are correctly specified in the batch and AutoHotkey scripts.
    Verify that PyQt5 and screen-brightness-control are installed correctly.
    Check the console output for any errors or messages that can help diagnose issues.
    Run the batch file manually to ensure it works as expected before using the AutoHotkey script.

Enjoy!