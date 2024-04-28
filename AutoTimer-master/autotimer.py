from __future__ import print_function
import time
import json
import datetime
import sys

# Platform-specific imports
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *
elif sys.platform in ['linux', 'linux2']:
    import linux as l

class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        _active_window_name = (NSWorkspace.sharedWorkspace()
                               .activeApplication()['NSApplicationName'])
    elif sys.platform in ['linux', 'linux2']:
        _active_window_name = l.get_active_window_x()
    return _active_window_name

def get_browser_url():
    url = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        if edit:
            url = edit.GetValuePattern().Value
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        textOfMyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
        s = NSAppleScript.initWithSource_(
            NSAppleScript.alloc(), textOfMyScript)
        results, err = s.executeAndReturnError_(None)
        url = results.stringValue()
    return url

def main():
    activeList = []
    previous_window = ""
    start_time = datetime.datetime.now()

    try:
        while True:
            current_window = get_active_window()
            if current_window != previous_window:
                print(current_window)
                if 'Google Chrome' in current_window:
                    url = get_browser_url()
                    if url:
                        print(url)
                previous_window = current_window
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")

if __name__ == "__main__":
    main()
