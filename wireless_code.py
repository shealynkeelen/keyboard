import time
import board
import digitalio
import wifi
import socketpool
import adafruit_requests
import pwmio
from analogio import AnalogIn

# Mac's IP address. found by hold "option" and press on wifi symbol on mac, then coppy the IP adress under wifi
MAC_IP = "xxxxxxxxxxx"

# Setup Network
# wifi.radio help the raspberry pi to get to the wifi networks
# SocketPool is the pipe that holds the pico datas to mac once they both are in the same wifi networks
# it’s called a Pool because the Pico can actually handle more than one connection at a time.
pool = socketpool.SocketPool(wifi.radio)

# requests uses that pool to actually send the data to the Mac
# .Session is the tool that stays in the pipe so the Pico can send data without restarting the connection.
# the Pool is the pipe, the Session is the water already inside it, ready to move the moment you turn the faucet.
requests = adafruit_requests.Session(pool)

# -------- BUTTON PINS --------
button_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,
    board.GP5, board.GP6, board.GP7, board.GP8
]

buttons = []
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.switch_to_input(pull=digitalio.Pull.UP)
    buttons.append(btn)


# -------- MODE BUTTON --------
mode_button = digitalio.DigitalInOut(board.GP20)
mode_button.switch_to_input(pull=digitalio.Pull.UP)

# -------- RGB LED --------
red = pwmio.PWMOut(board.GP18, frequency=1000, duty_cycle=0)
green = pwmio.PWMOut(board.GP17, frequency=1000, duty_cycle=0)
blue = pwmio.PWMOut(board.GP16, frequency=1000, duty_cycle=0)

# -------- POTENTIOMETER --------
pot = AnalogIn(board.GP26)

# --- STATE ---
brightness = 1.0
last_brightness = 0
current_mode = 0
mode_names = ["Professional", "Fun", "Coding"]
mode_paths = ["pro", "fun", "coding"]
last_mode_state = True
last_states = [True] * len(buttons)
colors = [
    (65535, 0, 0),
    (0, 65535, 0),
    (0, 0, 65535),
    (65535, 0, 65535),
    (65535, 65535, 0),
    (65535, 20000, 40000),
    (0, 65535, 65535),
    (65535, 30000, 30000),
    (30000, 65535, 30000)
]

color_names = ["RED", "GREEN", "BLUE", "PURPLE", "YELLOW", "PINK", "LIGHT BLUE", "LIGHT RED", "LIGHT GREEN"]

def set_color(r, g, b):
    red.duty_cycle = int(r * brightness)
    green.duty_cycle = int(g * brightness)
    blue.duty_cycle = int(b * brightness)

print("Wireless Macro Pad Active!")

print(f"Pico IP: {wifi.radio.ipv4_address}")
if wifi.radio.ipv4_address is None:
    print("❌ Pico is NOT connected to Wi-Fi. Check settings.toml!")

while True:
    active = False
    brightness = pot.value / 65535
    
    #if abs(brightness - last_brightness) > 0.02:
        #print("Brightness:", round(brightness, 2))
        #last_brightness = brightness
    
    # -------- MODE BUTTON HANDLING --------
    if last_mode_state and not mode_button.value:
        # Increment mode by 1
        current_mode = (current_mode + 1) % 3 
        
        print(f"Switched to {mode_names[current_mode]} Mode")
        try:
            response = requests.get(f"http://{MAC_IP}:5001/mode/{current_mode}")
            response.close()
        except Exception as e:
            print("Error:", e)
        time.sleep(0.25)  # debounce

    last_mode_state = mode_button.value

    # -------- BUTTON CHECK --------
    # Button Check
    for i in range(len(buttons)):
        if not buttons[i].value:
            r, g, b = colors[i]
            set_color(r, g, b)
            active = True
            
            if last_states[i]: # Trigger only on first press
                active_path = mode_paths[current_mode]

                # This sends the signal to the Mac using the "Building/Room" logic:
                # http://192.168.1.XX -> The Building (The Mac's IP)
                # :5001               -> The Entrance (The Port)
                # /macro1             -> The Specific Room (The Route)
                # We use rooms so Button 1 can go to /macro1 and Button 2 can go to /macro2
                try:
                    # requests.get sends signals to mac and also is use to receive signal from mac
                    # the code stops at this line until it receive a signal back from the mac
                    print('request sending...')
                    response = requests.get(f"http://{MAC_IP}:5001/{active_path}/{i}")
                    print(f"Sent {active_path} {i}: {response.text}")
                    print('finished!')
                    # response.close() is mandatory. Without it, the Pico will run out of memory 
                    # and the Wi-Fi 'pipe' will jam up after only a few button presses.
                    response.close()
                except Exception as e:
                    # Important for debugging
                    print("Error:", e)
        last_states[i] = buttons[i].value

    if not active:
        set_color(0, 0, 0)
    time.sleep(0.1)

