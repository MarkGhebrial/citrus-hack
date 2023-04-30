import pystray
import threading
import time
import platform

if platform.system() == "Linux":
    from linux_sensors import LinuxSensors as Sensors
elif platform.system() == "Windows":
    from windows_sensors import WindowsSensors as Sensors
else:
    exit("Platform {} not supported".format(platform.platform))

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
def generate_icon(num):
    width = 128
    height = 128

    picture = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(picture)
    d.font = ImageFont.truetype("fonts/RobotoCondensed-Bold.ttf", 75)
    
    d.text((-4, -15), str(num), align='center')

    d.font = ImageFont.truetype("fonts/RobotoCondensed-Bold.ttf", 45)
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

if __name__ == "__main__":

    sensors = Sensors()

    icon_thread = IconThread(Icon('TODO: Update Name', icon=generate_icon(0), menu=popUpMenu(sensors)))
    icon_thread.start()

    try:
        while True:
            time.sleep(1)
            icon_thread.icon.icon = generate_icon(sensors.get_power_consumption())
            icon_thread.icon.menu = popUpMenu(sensors)
            number += 1
    except KeyboardInterrupt:
        icon_thread.stop()
