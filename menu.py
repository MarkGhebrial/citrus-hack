import pystray
import threading
import time

from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageColor, ImageFont

# Menu that pops up on right click
def popUpMenu():
    menu = pystray.Menu(pystray.MenuItem('Cheese', on_clicked),
                        pystray.MenuItem('Config', on_clicked),
                        pystray.Menu.SEPARATOR,
                        pystray.MenuItem('Exit', on_clicked))

    return menu

def on_clicked(icon, item):
    global state
    state = not item.checked