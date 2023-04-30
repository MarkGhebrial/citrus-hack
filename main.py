import pystray
import threading
import time

from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageColor, ImageFont

clicks = []
number = 0

# Checks when the icon is clicked
def on_clicked(icon, item):
    print(icon)
    print(item)

# Make a 
def image(num):

    if number >= 50:
        txtColor = 'red'
    elif number > 16 and number < 50:
        txtColor = 'orange'
    else:
        txtColor = 'lime'

    width = 64
    height = 64

    picture = Image.new("RGB", (width, height), (0, 0, 0))
    d = ImageDraw.Draw(picture)
    d.font = ImageFont.truetype("Hack-Regular.ttf", 50)
    
    d.text((0, 0), str(num), fill=txtColor, align='center')

    return picture

class IconThread(threading.Thread):
    def __init__(self, *icon_args, **icon_kwargs):
        self.icon = None
        self._icon_args = icon_args
        self._icon_kwargs = icon_kwargs

        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self.icon = pystray.Icon(*self._icon_args, **self._icon_kwargs)
        def on_activate(icon):
            global number

            icon.icon = image(number)
            number += 1
        
        self.icon = Icon('test',
            icon=image(0),
            menu=menu(item('Toggle ', on_activate)))

        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()

icon_thread = IconThread('test name', menu=pystray.Menu(
            pystray.MenuItem(
                'Test Button', on_clicked)
            ),
        )
icon_thread.start()

try:
    while True:
        time.sleep(.1)
        icon_thread.icon.icon = image(number)
        number += 1
except KeyboardInterrupt:
    icon_thread.stop()
