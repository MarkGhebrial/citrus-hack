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
    width = 128
    height = 128

    picture = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    d = ImageDraw.Draw(picture)
    d.font = ImageFont.truetype("fonts/RobotoCondensed-Regular.ttf", 75)
    
    d.text((-3, -15), str(num), align='center')

    d.font = ImageFont.truetype("fonts/RobotoCondensed-Regular.ttf", 45)
    d.text((-2, 70), "WATTS", align="center")

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
