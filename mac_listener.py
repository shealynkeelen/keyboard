from flask import Flask # Flask use to catch the signals/datas from the "request" in code.py
import pyautogui # Once the signals/datas get into mac, PyautoGUI helps to hit the keys
import time
import os

# app = Flask(__name__) : Initializes the web server to listen for signals.
app = Flask(__name__)

@app.route('/mode/<int:index>')
def mode_change(index):
    mode_names = ["Professional", "Fun", "Coding"]
    print(f"Switched to {mode_names[index]} Mode")
    return f"Mode {index}"

# @app.route('/macro1') : Maps the specific web address to the macro function.
@app.route('/pro/<int:index>')
def professional_action(index):
    if index == 0:
        print("Action: Open YouTube link")
        os.system("open https://www.youtube.com/watch?v=jn9AFMKlGLA")
    elif index == 1:
        print("Action: Open Safari")
        os.system("open -a 'Safari'")
    elif index == 2:
        print("Action: Full screenshot")
        pyautogui.hotkey('command', 'shift', '3')
    elif index == 3:
        print("Action: Partial screenshot")
        pyautogui.hotkey('command', 'shift', '4') 
    elif index == 4:
        print("Action: Screen record menu")
        pyautogui.hotkey('command', 'shift', '5')
    elif index == 5:
        print("Action: Force Quit window")
        pyautogui.hotkey('option', 'command', 'escape')
    elif index == 6:
        print("Action: See all open windows")
        pyautogui.hotkey('ctrl', 'up')
    elif index == 7:
        print("Action: Type Ω")
        pyautogui.hotkey('option', 'z')
    elif index == 8:
        # This can only be done on Safari
        print("Action: Summarize texts")
        pyautogui.hotkey('shift', 'command', 'r')
    return f"Pro {index} Triggered"

@app.route('/fun/<int:index>')
def fun_action(index):
    if index == 0:
        print("Fun Mode Action: Open calender & add new event")
        os.system("open -a 'Calendar'")
        time.sleep(1)
        pyautogui.hotkey('command', 'n')
    elif index == 1:
        # Use this command when in Finder or Google Chrome or Safari
        print("Fun Mode Action: Open the downloads folder")
        pyautogui.hotkey('option', 'command', 'l')
    elif index == 2:
        print("Fun Mode Action: Open Photo Booth")
        os.system("open -a 'photo booth'")
    elif index == 3:
        print("Fun Mode Action: Open Weather App")
        os.system("open -a 'weather'")
    elif index == 4:
        print("Fun Mode Action: Shealyn's cat!")
        # This tells the Mac system directly: "Open this specific file"
        # No typing, no Spotlight, no iMessage mistakes!
        file_path = os.path.expanduser("~/Documents/Project2_Macro_Keyboard/Cat.HEIC")
        os.system(f"open '{file_path}'")
    elif index == 5:
        print("Fun Mode Action: Chess")
        os.system("open -a 'Chess'")
    elif index == 6:
        print("Fun Mode Action: Emojis")
        pyautogui.hotkey('ctrl', 'command', 'space')
    elif index == 7:
        # To do this, go to system settings -> keyboard -> keyboard shortcuts -> Accessibility -> check Contrast and Invert colors
        # Ten System settings -> Accessebility -> Display -> Turn on Invert colors once and then turn off
        print("Fun Mode Action: Invert Color")
        pyautogui.hotkey('ctrl', 'option', 'command', '8') 
    elif index == 8:
        print("Fun Mode: Bonjour! Opening cat photo")
        # Change 'Downloads' to 'Desktop' if that's where you saved it!
        script = "tell application \"Photos\" to set container to (search for \"IMG_2592\")"
        os.system(f"osascript -e '{script}'")
        os.system("open -a 'Photos'")
    return f"Fun {index} Triggered"

@app.route('/coding/<int:index>')
def coding_action(index):
    if index == 0:
        print("Code Mode Action: Open VScode")
        os.system("open -a 'Visual Studio Code'")
    elif index == 1:
        print("Code Mode Acion: Open GitHub Desktop")
        os.system("open -a 'GitHub Desktop'")
    elif index == 2:
        # Use this if want to open a specific folder or file
        print("Code Mode Action: Choose To Open")
        pyautogui.hotkey('command', 'o')
    elif index == 3:
        # Only does this when you already selected the codes that you wanted
        print("Code Mode Action: Open in line chat")
        pyautogui.hotkey('command', 'i')
    elif index == 4: # 4 is doing 3, 5 is doing 4 works, 6 is doing 5 works, 7 doing 6 works, 8 is doing 7 works, 8 doesnt do anything
        # Only does this when you already selected the codes that you wanted
        print("Code Mode Action: Edit all code of the same type at once")
        pyautogui.hotkey('command', 'shift', 'l')
    elif index == 5:
        print("Code Mode Action: Comment/Uncomment line(s)")
        pyautogui.hotkey('command', '/')
    elif index == 6:
        print("Code Mode Action: Toggle terminal on/off")
        pyautogui.hotkey('ctrl', '`')
    elif index == 7:
        # Select a variable name for this to work
        print("Code Mode Action: Open small window of the same code file")
        pyautogui.hotkey('fn', 'option', 'f12')
    elif index == 8:
        print("Code Mode Action: Open side by side code window of the same file")
        pyautogui.hotkey('command', '\\')
    return f"Coding {index} Triggered"
        
        
if __name__ == '__main__':
    # '0.0.0.0' allows the Pico to find the Mac on the network
    app.run(host='0.0.0.0', port=5001)
