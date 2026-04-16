import time
import board
import digitalio
import pwmio
import usb_hid
from analogio import AnalogIn

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# -------- BUTTON PINS --------
button_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,
    board.GP16, board.GP17, board.GP18, board.GP19
]

buttons = []
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

# -------- MODE BUTTON --------
mode_button = digitalio.DigitalInOut(board.GP15)
mode_button.direction = digitalio.Direction.INPUT
mode_button.pull = digitalio.Pull.UP

# -------- RGB LED --------
red = pwmio.PWMOut(board.GP22, frequency=1000, duty_cycle=0)
green = pwmio.PWMOut(board.GP21, frequency=1000, duty_cycle=0)
blue = pwmio.PWMOut(board.GP20, frequency=1000, duty_cycle=0)

# -------- POTENTIOMETER --------
pot = AnalogIn(board.GP26)

# -------- HID SETUP --------
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# -------- BRIGHTNESS --------
brightness = 1.0
last_brightness = 0

# -------- MODE STATE --------
professional_mode = True
last_mode_state = True

def set_color(r, g, b):
    red.duty_cycle = int(r * brightness)
    green.duty_cycle = int(g * brightness)
    blue.duty_cycle = int(b * brightness)

# -------- COLORS --------
colors = [
    (65535, 0, 0),         # button 0 = red
    (0, 65535, 0),         # button 1 = green
    (0, 0, 65535),         # button 2 = blue
    (65535, 0, 65535),     # button 3 = purple
    (65535, 65535, 0),     # button 4 = yellow
    (65535, 20000, 40000), # button 5 = pink
    (0, 65535, 65535),     # button 6 = light blue
    (65535, 30000, 30000), # button 7 = light red
    (30000, 65535, 30000)  # button 8 = light green
]

color_names = [
    "RED",
    "GREEN",
    "BLUE",
    "PURPLE",
    "YELLOW",
    "PINK",
    "LIGHT BLUE",
    "LIGHT RED",
    "LIGHT GREEN"
]

def press_shortcut(*keys, wait=0.15):
    keyboard.send(*keys)
    time.sleep(wait)

def open_spotlight_and_type(text):
    keyboard.send(Keycode.COMMAND, Keycode.SPACE)
    time.sleep(0.5)
    layout.write(text)
    time.sleep(0.2)
    keyboard.send(Keycode.ENTER)
    time.sleep(0.3)

def do_professional_action(index):
    if index == 0:
        print("Action: Open YouTube link")
        keyboard.send(Keycode.COMMAND, Keycode.SPACE)
        time.sleep(0.5)
        layout.write("https://www.youtube.com/watch?v=jn9AFMKlGLA")
        time.sleep(0.2)
        keyboard.send(Keycode.ENTER)

    elif index == 1:
        print("Action: Open Chrome")
        open_spotlight_and_type("Google Chrome")

    elif index == 2:
        print("Action: Full screenshot")
        press_shortcut(Keycode.COMMAND, Keycode.SHIFT, Keycode.THREE)

    elif index == 3:
        print("Action: Partial screenshot")
        press_shortcut(Keycode.COMMAND, Keycode.SHIFT, Keycode.FOUR)

    elif index == 4:
        print("Action: Screen record menu")
        press_shortcut(Keycode.COMMAND, Keycode.SHIFT, Keycode.FIVE)

    elif index == 5:
        print("Action: Force Quit window")
        press_shortcut(Keycode.OPTION, Keycode.COMMAND, Keycode.ESCAPE)

    elif index == 6:
        print("Action: See all open windows")
        press_shortcut(Keycode.CONTROL, Keycode.UP_ARROW)

    elif index == 7:
        print("Action: Type Ω")
        keyboard.send(Keycode.OPTION, Keycode.Z)
        time.sleep(0.15)

    elif index == 8:
        print("Action: Command + Z")
        press_shortcut(Keycode.COMMAND, Keycode.Z)

def do_fun_action(index):
    if index == 0:
        print("Fun Mode Action: Control + F")
        press_shortcut(Keycode.CONTROL, Keycode.F)

    elif index == 1:
        print("Fun Mode Action: Command + C")
        press_shortcut(Keycode.COMMAND, Keycode.C)

    elif index == 2:
        print("Fun Mode Action: Command + V")
        press_shortcut(Keycode.COMMAND, Keycode.V)

    elif index == 3:
        print("Fun Mode Action: Command + N")
        press_shortcut(Keycode.COMMAND, Keycode.N)

    elif index == 4:
        print("Fun Mode: Button 4 pressed")

    elif index == 5:
        print("Fun Mode: Button 5 pressed")

    elif index == 6:
        print("Fun Mode: Button 6 pressed")

    elif index == 7:
        print("Fun Mode: Button 7 pressed")

    elif index == 8:
        print("Fun Mode: Button 8 pressed")

# -------- START OFF --------
set_color(0, 0, 0)

last_states = [True] * len(buttons)

print("Professional Mode")

# -------- MAIN LOOP --------
while True:
    active = False

    # -------- POTENTIOMETER BRIGHTNESS CONTROL --------
    pot_value = pot.value
    brightness = pot_value / 65535

    if abs(brightness - last_brightness) > 0.02:
        print("Brightness:", round(brightness, 2))
        last_brightness = brightness

    # -------- MODE BUTTON HANDLING --------
    current_mode_state = mode_button.value

    if last_mode_state and not current_mode_state:
        professional_mode = not professional_mode

        if professional_mode:
            print("Professional Mode")
        else:
            print("Fun Mode")

        time.sleep(0.25)  # debounce

    last_mode_state = current_mode_state

    # -------- BUTTON HANDLING --------
    for i in range(len(buttons)):
        current_state = buttons[i].value

        if last_states[i] and not current_state:
            r, g, b = colors[i]
            set_color(r, g, b)
            print("Button", i, "pressed -> Color:", color_names[i])

            if professional_mode:
                do_professional_action(i)
            else:
                do_fun_action(i)

            active = True

        if not current_state:
            r, g, b = colors[i]
            set_color(r, g, b)
            active = True

        last_states[i] = current_state

    if not active:
        set_color(0, 0, 0)

    time.sleep(0.03)