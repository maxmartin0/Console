from console import Console
from utime import sleep
from sys import exit as reboot
from image import startingScreen

sleep(0.5)

console = Console()

class Main:
    def __init__(self):
        console.oled.clear()
        console.oled.show()
        print(f'\n\nMAX CONSOLE\n-----------\nConsole Version:   {console.VERSION}\nMicro Controler:   RPi Pico\n       Language:   Micro Python\n         Screen:   OLED 0.96" SSD1305')
        self.start()
    def start(self):
        console.oled.image(startingScreen)
        console.oled.show()
        sleep(1)
        console.oled.invert()
        console.oled.show()
        sleep(0.5)
        console.oled.clear()
        console.oled.invert(False)
        console.oled.show()



Main()
