import pystray
import threading
import time

from sensor_interface import *

from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageColor, ImageFont

procs = []

# Generate the menu that appears when the icon is right-clicked
def popUpMenu(sensors: Sensors):
    global procs

    # Update the list of Processes. TODO: Do this efficiently
    new_procs = sensors.get_process_list()
    for new_proc in new_procs:
        if new_proc not in procs:
            procs.append(new_proc)
    for proc in procs:
        if proc not in new_procs:
            procs.remove(proc)

    # Calculate the CPU load of each process
    proc_list = []
    for p in procs:
        proc_list.append((p, p.get_cpu_percent()))

    # Sort the list of processes by CPU usage (highest first)
    proc_list.sort(key=lambda proc: proc[1], reverse=True)

    # Menu layout
    #   List of the most resource-intensive processes
    #   ~~~ Separator ~~~
    #   Button to exit the application
    menu = []

    for i in range(5):
        menu.append(
            item(
                "{}: {}%".format(proc_list[i][0].name, proc_list[i][1]),
                None # No action when clicked
            )
        )
    
    menu.append(pystray.Menu.SEPARATOR)
    menu.append(item('Exit', None))

    return pystray.Menu(*menu)

    return menu

def on_clicked(icon, item):
    global state
    state = not item.checked