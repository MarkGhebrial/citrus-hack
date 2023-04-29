App lives in system tray

Features
- Tracks battery usage/power consumption per process
  - File that contains the power draw in microwatts: `/sys/class/power_supply/BAT0/power_now`
- Tracks display power consumption
- Tracks usb device power consumption
- Tells you what process uses the most power
- Make reccomendations for reducing power consumption
- Put laptop into preset low power mode
  - Automatically turn off RGB
  - Underclock CPU
  - Reduce brightness
- Warn user of high power consumption from a device or process

When you click on the app:
- You see
  - A list of the processes that are consuming the most power
  - Power consumption of usb devices
  - Power consumtion of the whole system
  - Power consumtion of the display
  - A menu with options to:
    - Enter ultra-low-power mode
  - 