import pyautogui
import time

def setup(setup_time, shortcut_key):
  if shortcut_key:
    pyautogui.hotkey('winleft', '4')
    time.sleep(0.5)
  else:
    time.sleep(setup_time)
  pyautogui.hotkey('ctrl', 'shift', 'n')
  time.sleep(0.2)
  pyautogui.typewrite('https://www.nytimes.com/games/wordle/index.html')
  pyautogui.press('enter')
  time.sleep(1)
  for i in range(0,2):
    pyautogui.click(1448, 848)
    
if __name__ == '__main__':
  setup(3, True)