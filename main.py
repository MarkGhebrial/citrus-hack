import pystray
import threading
import time

from linux_sensors import LinuxSensors

from menu import popUpMenu
from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageColor, ImageFont

clicks = []
number = 0

# Checks when the icon is clicked
def on_clicked(icon, item):
    print(icon)
    print(item)

# Make an image using numbers
def image(num):

    if number >= 50:
        txtColor = 'red'
    elif number > 16 and number < 50:
        txtColor = 'orange'
    else:
        txtColor = 'lime'

    width = 64
    height = 64

    picture = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(picture)
    d.font = ImageFont.truetype("Hack-Regular.ttf", 40)
    
    d.text((0, 0), str(num), fill=txtColor, align='center')

    return picture

class IconThread(threading.Thread):
    def __init__(self, icon):
        self.icon = icon

        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()

icon_thread = IconThread(Icon('TODO: Update Name', icon=image(0), menu=popUpMenu(LinuxSensors())))
icon_thread.start()

try:
    while True:
        time.sleep(1)
        icon_thread.icon.icon = image(LinuxSensors().get_power_consumption())
        icon_thread.icon.menu = popUpMenu(LinuxSensors())
        number += 1
except KeyboardInterrupt:
    icon_thread.stop()
