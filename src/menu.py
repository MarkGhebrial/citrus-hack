import pystray
import threading
import time

from sensor_interface import *

from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageColor, ImageFont

# Generate the menu that appears when the icon is right-clicked
def popUpMenu(sensors: Sensors):
    
    procs = sensors.get_process_list()

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
                "{percent:>.2f}%: {name}".format(name=proc_list[i][0].name, percent=proc_list[i][1]),
                None # No action when clicked
            )
        )
    
    menu.append(pystray.Menu.SEPARATOR)
    menu.append(item('Exit', None))

    return pystray.Menu(*menu)
