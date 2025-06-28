import pyautogui
import time
import os

pyautogui.FAILSAFE = True

# Show desktop (Windows only)
pyautogui.hotkey('win', 'd')
time.sleep(2)

print("Opening folder in 3 seconds...")
time.sleep(3)

# Folder coordinates (use accurate values from position test)
folder_coords = (790, 143)  # CHANGE this to your folder's position
pyautogui.moveTo(folder_coords[0], folder_coords[1], duration=1)
pyautogui.doubleClick()

# Optional fallback
folder_name = "spotify-full-stack"  # Replace with folder name
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", folder_name)
if os.path.exists(desktop_path):
    time.sleep(1)
    os.startfile(desktop_path)
