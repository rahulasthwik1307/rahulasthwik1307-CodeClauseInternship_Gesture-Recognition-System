import ctypes
import time

# Standard arrow key codes
right_pressed = 0x27  # Right arrow
left_pressed = 0x25    # Left arrow

# Enhanced key press with error handling
def PressKey(hexKeyCode):
    try:
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0, 0)
    except Exception as e:
        print(f"Key press error: {e}")

def ReleaseKey(hexKeyCode):
    try:
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0x0002, 0)
    except Exception as e:
        print(f"Key release error: {e}")

def KeyIsPressed(hexKeyCode):
    return ctypes.windll.user32.GetAsyncKeyState(hexKeyCode) & 0x8000 != 0