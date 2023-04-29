import pystray
import threading
import time

from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageColor

clicks = []

# Creates an image with a colored pattern
def create_image():
    bgColor = input("Enter a background color: ")
    frColor1 = input("Enter a color: ")
    frColor2 = input("Enter a second color: ")

    width = 512
    height = 512
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), ImageColor.getrgb(bgColor))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=ImageColor.getrgb(frColor1))
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=ImageColor.getrgb(frColor2))

    return image

# Checks when the icon is clicked
def on_clicked(icon, item):
    print(icon)
    print(item)

def image(): # color1, color2, width=512, height=512
    #bgColor = input("Enter a background color: ")
    frColor1 = input("Enter a color: ")
    frColor2 = input("Enter a second color: ")

    width = 512
    height = 512

    image = Image.new('RGB', (width, height), frColor1)
    dc = ImageDraw.Draw(image)

    dc.rectangle((width // 2, 0, width, height // 2), fill=frColor2)
    dc.rectangle((0, height // 2, width // 2, height), fill=frColor2)

    return image

class IconThread(threading.Thread):
    def __init__(self, *icon_args, **icon_kwargs):
        self.icon = None
        self._icon_args = icon_args
        self._icon_kwargs = icon_kwargs

        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self.icon = pystray.Icon(*self._icon_args, **self._icon_kwargs)
        def on_activate(icon):
            clicks.append(icon)

            if len(clicks) == 5:
                icon.stop()
            else:
                icon.icon = images[len(clicks) % len(images)]

        images = (image(), image())
        self.icon = Icon(
            'test',
            icon=images[0],
            menu=menu(item('Toggle ', on_activate)))

        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()

icon_thread = IconThread('test name', menu=pystray.Menu(
            pystray.MenuItem(
                'Test Button', on_clicked)
            )
        )
icon_thread.start()

try:
    while True:
        time.sleep(.1)
except KeyboardInterrupt:
    icon_thread.stop()
