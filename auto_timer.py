import win32gui
from time import sleep
from monitor import *
import json
import datetime
import time , sys


active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True

def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    return _active_window_name

try:
    activeList.initialize_me()
except Exception:
    print('No json.So creating a json file!')

try:
    while True:
        new_window_name = get_active_window()

        if active_window_name != new_window_name:
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)

                if not exists:
                    activity = Activity(activity_name,[time_entry])
                    activeList.activities.append(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name
            print("Monitoring:",active_window_name)
        time.sleep(1)
    
except KeyboardInterrupt:
    with open('activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4)
    print('Stopped monitoring!')


print("*" * 60)
with open("activities.json") as read_json:
    print(read_json.read())
