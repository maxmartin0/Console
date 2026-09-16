from machine import Pin, I2C
import framebuf
import time


# ============================================================
# 5x8 FONT
# ============================================================

# We use MicroPython's built in FrameBuffer.text()
# so no font table is required.


# ============================================================
# OLED DRIVER
# ============================================================

class OLED:

    def __init__(
        self,
        width=128,
        height=64,
        sda=0,
        scl=1,
        addr=0x3C,
        freq=400000
    ):

        self.width = width
        self.height = height

        self.i2c = I2C(
            0,
            sda=Pin(sda),
            scl=Pin(scl),
            freq=freq
        )

        self.buffer = bytearray(width * height // 8)

        self.fb = framebuf.FrameBuffer(
            self.buffer,
            width,
            height,
            framebuf.MONO_VLSB
        )

        self.addr = addr

        self._init_display()

    # ----------------------------------------------------

    def _write_cmd(self, cmd):
        self.i2c.writeto(
            self.addr,
            bytes([0x80, cmd])
        )

    def _write_data(self):
        self.i2c.writeto(
            self.addr,
            b"\x40" + self.buffer
        )

    # ----------------------------------------------------

    def _init_display(self):

        cmds = [

            0xAE,
            0x20, 0x00,

            0x40,

            0xA1,

            0xC8,

            0x81, 0xCF,

            0xA6,

            0xA8, 0x3F,

            0xD3, 0x00,

            0xD5, 0x80,

            0xD9, 0xF1,

            0xDA, 0x12,

            0xDB, 0x40,

            0x8D, 0x14,

            0xAF

        ]

        for c in cmds:
            self._write_cmd(c)

        self.clear()

    # ----------------------------------------------------

    def show(self):

        self._write_cmd(0x21)
        self._write_cmd(0)
        self._write_cmd(self.width - 1)

        self._write_cmd(0x22)
        self._write_cmd(0)
        self._write_cmd((self.height // 8) - 1)

        self._write_data()

    # ----------------------------------------------------

    def clear(self):

        self.fb.fill(0)

    def fill(self):

        self.fb.fill(1)

    def pixel(self, x, y, colour=1):

        self.fb.pixel(x, y, colour)

    def text(self, text, x=0, y=0):

        self.fb.text(
            str(text),
            x,
            y,
            1
        )

    def line(self, x1, y1, x2, y2, colour=1):

        self.fb.line(
            x1,
            y1,
            x2,
            y2,
            colour
        )

    def rect(
        self,
        x,
        y,
        w,
        h,
        colour=1
    ):

        self.fb.rect(
            x,
            y,
            w,
            h,
            colour
        )

    def fill_rect(
        self,
        x,
        y,
        w,
        h,
        colour=1
    ):

        self.fb.fill_rect(
            x,
            y,
            w,
            h,
            colour
        )
    
    def image(self, bitmap, x = 0, y = 0, width = 128, height = 64):

        img = framebuf.FrameBuffer(
            bitmap,
            width,
            height,
            framebuf.MONO_VLSB
        )

        self.fb.blit(img, x, y)
    # ----------------------------------------------------

    def circle(self, x0, y0, r, colour=1):

        x = r
        y = 0
        err = 1 - r

        while x >= y:

            self.pixel(x0 + x, y0 + y, colour)
            self.pixel(x0 + y, y0 + x, colour)
            self.pixel(x0 - y, y0 + x, colour)
            self.pixel(x0 - x, y0 + y, colour)

            self.pixel(x0 - x, y0 - y, colour)
            self.pixel(x0 - y, y0 - x, colour)
            self.pixel(x0 + y, y0 - x, colour)
            self.pixel(x0 + x, y0 - y, colour)

            y += 1

            if err < 0:
                err += (2 * y) + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    # ----------------------------------------------------

    def invert(self, value=True):

        self._write_cmd(0xA7 if value else 0xA6)

    # ----------------------------------------------------

    def contrast(self, value):

        value = max(0, min(255, int(value)))

        self._write_cmd(0x81)
        self._write_cmd(value)


# ============================================================
# BUTTON
# ============================================================

class Button:

    def __init__(self, pin):

        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def __bool__(self):

        return self.pin.value() == 0

    def value(self):

        return self.pin.value() == 0


# ============================================================
# BUTTON COLLECTION
# ============================================================

class Buttons:

    def __init__(
        self,
        up=14,
        down=12,
        left=13,
        right=15
    ):

        self.up = Button(up)
        self.down = Button(down)
        self.left = Button(left)
        self.right = Button(right)

    # ----------------------------------------------------

    def any(self):

        return (
            self.up or
            self.down or
            self.left or
            self.right
        )

    # ----------------------------------------------------

    def wait(self):

        while True:

            if self.up:
                while self.up:
                    time.sleep_ms(10)
                return self.up

            if self.down:
                while self.down:
                    time.sleep_ms(10)
                return self.down

            if self.left:
                while self.left:
                    time.sleep_ms(10)
                return self.left

            if self.right:
                while self.right:
                    time.sleep_ms(10)
                return self.right

            time.sleep_ms(5)
# ============================================================
# CONSOLE
# ============================================================

class Console:

    VERSION = "1.2"

    def __init__(
        self,
        sda=0,
        scl=1,
        up=14,
        down=12,
        left=13,
        right=15
    ):

        self.oled = OLED(
            sda=sda,
            scl=scl
        )

        self.button = Buttons(
            up=up,
            down=down,
            left=left,
            right=right
        )

    # ----------------------------------------------------

    def sleep(self, milliseconds):

        time.sleep_ms(milliseconds)


# ============================================================
# END OF LIBRARY
# ============================================================
