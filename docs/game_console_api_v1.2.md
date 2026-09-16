# Game Console API Guide

**API version:** `1.2`  
**Platform:** Raspberry Pi Pico / MicroPython  
**Display:** 128×64 I2C OLED  
**Library style:** Simple object-based API

---

## 1. Getting Started

Save the console library as something such as:

```text
console.py
```

Then in your game:

```python
from console import Console

console = Console()
```

The `Console` object provides:

- `console.oled` — OLED graphics
- `console.button` — directional buttons
- `console.sleep()` — millisecond delays

A basic program:

```python
from console import Console

console = Console()

console.oled.text("Hello!", 0, 0)
console.oled.show()
```

---

# 2. Console

## `Console()`

Creates a console object.

```python
console = Console()
```

### Parameters

| Parameter | Default | Description |
|---|---:|---|
| `sda` | `0` | Pico GPIO used for I2C SDA |
| `scl` | `1` | Pico GPIO used for I2C SCL |
| `up` | `14` | GPIO for the UP button |
| `down` | `12` | GPIO for the DOWN button |
| `left` | `13` | GPIO for the LEFT button |
| `right` | `15` | GPIO for the RIGHT button |

Example with custom pins:

```python
console = Console(
    sda=0,
    scl=1,
    up=14,
    down=12,
    left=13,
    right=15
)
```

## `Console.VERSION`

Contains the API version.

```python
print(console.VERSION)
```

Output:

```text
1.2
```

---

## `console.sleep(milliseconds)`

Pauses the program for a specified number of milliseconds.

```python
console.sleep(500)
```

This waits for 500 ms (half a second).

Example:

```python
console.oled.text("Hello", 0, 0)
console.oled.show()

console.sleep(1000)

console.oled.clear()
console.oled.show()
```

---

# 3. OLED

The OLED is available through:

```python
console.oled
```

The default display size is:

```text
128 × 64 pixels
```

Coordinates start at the **top-left corner**:

```text
(0, 0) ───────────────────► X
  │
  │
  │
  │
  ▼
  Y
```

Therefore:

- `x = 0` is the left edge
- `x = 127` is the right edge
- `y = 0` is the top edge
- `y = 63` is the bottom edge

---

# 4. OLED Text

## `oled.text(text, x=0, y=0)`

Draws text on the display.

```python
console.oled.text("Hello", 0, 0)
```

The text is drawn into the display buffer. You normally need to call `show()` afterwards.

```python
console.oled.text("Hello", 0, 0)
console.oled.show()
```

`text` is converted to a string automatically, so this works too:

```python
score = 42

console.oled.text(score, 0, 0)
console.oled.show()
```

---

# 5. Updating the Display

## `oled.show()`

Sends the current display buffer to the physical OLED.

```python
console.oled.show()
```

Most drawing functions do **not** immediately update the physical screen.

For example:

```python
console.oled.clear()
console.oled.text("Hello", 0, 0)
console.oled.rect(20, 20, 50, 30)

console.oled.show()
```

This is useful because several things can be drawn before updating the screen.

---

# 6. Clearing and Filling

## `oled.clear()`

Clears the display buffer.

```python
console.oled.clear()
```

To actually clear the physical screen:

```python
console.oled.clear()
console.oled.show()
```

---

## `oled.fill()`

Fills the entire display buffer with pixels.

```python
console.oled.fill()
console.oled.show()
```

This makes the entire display light up.

---

# 7. Pixels

## `oled.pixel(x, y, colour=1)`

Changes a single pixel.

```python
console.oled.pixel(10, 20)
```

The default colour is `1` (on).

To turn a pixel off:

```python
console.oled.pixel(10, 20, 0)
```

Example:

```python
console.oled.clear()

for x in range(128):
    console.oled.pixel(x, 32)

console.oled.show()
```

---

# 8. Lines

## `oled.line(x1, y1, x2, y2, colour=1)`

Draws a line between two points.

```python
console.oled.line(0, 0, 127, 63)
```

Parameters:

| Parameter | Description |
|---|---|
| `x1` | Starting X |
| `y1` | Starting Y |
| `x2` | Ending X |
| `y2` | Ending Y |
| `colour` | `1` for on, `0` for off |

Example:

```python
console.oled.clear()

console.oled.line(0, 0, 127, 63)
console.oled.line(127, 0, 0, 63)

console.oled.show()
```

---

# 9. Rectangles

## `oled.rect(x, y, w, h, colour=1)`

Draws an outline rectangle.

```python
console.oled.rect(10, 10, 50, 30)
```

Parameters:

| Parameter | Description |
|---|---|
| `x` | Left position |
| `y` | Top position |
| `w` | Width |
| `h` | Height |
| `colour` | `1` for on, `0` for off |

Example:

```python
console.oled.clear()

console.oled.rect(20, 15, 80, 35)

console.oled.show()
```

---

## `oled.fill_rect(x, y, w, h, colour=1)`

Draws a filled rectangle.

```python
console.oled.fill_rect(20, 15, 80, 35)
```

Example:

```python
console.oled.clear()

console.oled.fill_rect(10, 10, 30, 30)

console.oled.show()
```

---

# 10. Circles

## `oled.circle(x0, y0, r, colour=1)`

Draws an outline circle.

```python
console.oled.circle(64, 32, 20)
```

Parameters:

| Parameter | Description |
|---|---|
| `x0` | Centre X |
| `y0` | Centre Y |
| `r` | Radius |
| `colour` | `1` for on, `0` for off |

Example:

```python
console.oled.clear()

console.oled.circle(64, 32, 20)

console.oled.show()
```

The circle is not filled.

A filled circle can be made by drawing multiple circles with decreasing radii, or by using filled shapes made from other primitives.

---

# 11. Images / Bitmaps

## `oled.image(bitmap, x=0, y=0, width=128, height=64)`

Draws a bitmap onto the display.

The bitmap must be compatible with MicroPython's `framebuf.FrameBuffer` using:

```python
framebuf.MONO_VLSB
```

Example:

```python
bitmap = bytearray([
    # bitmap data here
])

console.oled.image(
    bitmap,
    x=0,
    y=0,
    width=16,
    height=16
)

console.oled.show()
```

### Important

The `width` and `height` parameters must match the dimensions of the bitmap.

For a 128×64 bitmap, you can simply use:

```python
console.oled.image(bitmap)
```

---

# 12. Inverting the Display

## `oled.invert(value=True)`

Inverts the physical OLED display.

```python
console.oled.invert()
```

To return to normal:

```python
console.oled.invert(False)
```

This changes the OLED display mode directly.

---

# 13. OLED Contrast

## `oled.contrast(value)`

Changes the OLED contrast.

The value is automatically limited to the range:

```text
0–255
```

Example:

```python
console.oled.contrast(128)
```

Maximum contrast:

```python
console.oled.contrast(255)
```

Minimum contrast:

```python
console.oled.contrast(0)
```

---

# 14. Buttons

Buttons are available through:

```python
console.button
```

There are four buttons:

```python
console.button.up
console.button.down
console.button.left
console.button.right
```

The buttons use the Pico's internal pull-up resistors.

A button evaluates to `True` while it is pressed.

---

# 15. Checking Buttons

## `button.value()`

Returns:

```text
True  = pressed
False = not pressed
```

Example:

```python
if console.button.up.value():
    print("UP pressed")
```

---

## Boolean Button Checking

Buttons can also be used directly in `if` statements:

```python
if console.button.up:
    print("UP pressed")
```

This is the recommended simple way to check a button.

Example:

```python
while True:

    if console.button.up:
        print("UP")

    if console.button.down:
        print("DOWN")

    if console.button.left:
        print("LEFT")

    if console.button.right:
        print("RIGHT")

    console.sleep(10)
```

---

# 16. Checking Any Button

## `button.any()`

Returns `True` if **any** of the four buttons is currently pressed.

```python
if console.button.any():
    print("A button is pressed")
```

Example:

```python
while not console.button.any():
    console.sleep(10)

print("Button pressed!")
```

---

# 17. Waiting for a Button

## `button.wait()`

Waits until one of the buttons is pressed.

```python
console.button.wait()
```

The function waits until:

- UP is pressed
- DOWN is pressed
- LEFT is pressed
- RIGHT is pressed

It then waits for that button to be released before returning.

Example:

```python
console.oled.clear()
console.oled.text("Press a button", 0, 0)
console.oled.show()

console.button.wait()

console.oled.clear()
console.oled.text("Button pressed!", 0, 0)
console.oled.show()
```

### Important note

The current implementation returns the `Button` object that was detected.

For example:

```python
button = console.button.wait()

if button is console.button.up:
    print("UP")

elif button is console.button.down:
    print("DOWN")

elif button is console.button.left:
    print("LEFT")

elif button is console.button.right:
    print("RIGHT")
```

---

# 18. Example Game Loop

A simple game can use the API like this:

```python
from console import Console

console = Console()

x = 60
y = 30

while True:

    # Input
    if console.button.up:
        y -= 1

    if console.button.down:
        y += 1

    if console.button.left:
        x -= 1

    if console.button.right:
        x += 1

    # Draw
    console.oled.clear()

    console.oled.circle(x, y, 5)

    console.oled.show()

    # Small delay
    console.sleep(20)
```

This creates a small circle that can be moved around the screen using the four buttons.

---

# 19. Example Menu

The button API can also be used to make menus.

```python
from console import Console

console = Console()

options = [
    "Start Game",
    "Settings",
    "About"
]

selected = 0

while True:

    console.oled.clear()

    for i, option in enumerate(options):

        prefix = ">" if i == selected else " "

        console.oled.text(
            prefix + option,
            10,
            i * 16
        )

    console.oled.show()

    if console.button.up:
        selected -= 1

        if selected < 0:
            selected = len(options) - 1

        console.sleep(150)

    if console.button.down:
        selected += 1

        if selected >= len(options):
            selected = 0

        console.sleep(150)

    if console.button.left:
        print("LEFT")

        console.sleep(150)

    if console.button.right:
        print("RIGHT")

        console.sleep(150)

    console.sleep(10)
```

---

# 20. Complete API Reference

## Console

| API | Description |
|---|---|
| `Console()` | Creates a console |
| `console.VERSION` | Returns the API version |
| `console.sleep(ms)` | Sleeps for milliseconds |

## OLED

| API | Description |
|---|---|
| `console.oled.show()` | Sends buffer to OLED |
| `console.oled.clear()` | Clears display buffer |
| `console.oled.fill()` | Fills display buffer |
| `console.oled.pixel(x, y, colour)` | Draws a pixel |
| `console.oled.text(text, x, y)` | Draws text |
| `console.oled.line(x1, y1, x2, y2, colour)` | Draws a line |
| `console.oled.rect(x, y, w, h, colour)` | Draws a rectangle |
| `console.oled.fill_rect(x, y, w, h, colour)` | Draws a filled rectangle |
| `console.oled.circle(x, y, r, colour)` | Draws a circle |
| `console.oled.image(bitmap, x, y, width, height)` | Draws a bitmap |
| `console.oled.invert(value)` | Inverts the OLED |
| `console.oled.contrast(value)` | Sets OLED contrast |

## Buttons

| API | Description |
|---|---|
| `console.button.up` | UP button |
| `console.button.down` | DOWN button |
| `console.button.left` | LEFT button |
| `console.button.right` | RIGHT button |
| `console.button.any()` | Checks whether any button is pressed |
| `console.button.wait()` | Waits for a button press |
| `button.value()` | Checks an individual button |

---

# 21. Default Hardware Pinout

The default API configuration uses:

| Component | Pico GPIO |
|---|---:|
| OLED SDA | GP0 |
| OLED SCL | GP1 |
| UP | GP14 |
| DOWN | GP12 |
| LEFT | GP13 |
| RIGHT | GP15 |

The pins can be changed when creating the `Console` object.

```python
console = Console(
    sda=0,
    scl=1,
    up=14,
    down=12,
    left=13,
    right=15
)
```

---

# 22. API Philosophy

The console API is designed so that games do not need to deal directly with:

- `machine.Pin`
- `machine.I2C`
- `framebuf.FrameBuffer`
- OLED initialization commands
- button pull-up configuration
- button polling implementation

Instead, a game can use a simple interface:

```python
console.oled.text("My Game", 0, 0)

if console.button.up:
    player_y -= 1

console.oled.show()
```

This keeps individual games small and makes the hardware details part of the console library.

---

# 23. Version

Current API version:

```text
1.2
```

The version is available in Python as:

```python
Console.VERSION
```

When the API changes in a way that affects games, the version should be updated.
