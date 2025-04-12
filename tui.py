# Non-default libraries (e.g curses) were disallowed for this project

import ctypes

class Keys():
    # From https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    vk_codes = {
        " ": 0x20,
        "up": 0x26,
        "down": 0x28,
        "left": 0x25,
        "right": 0x27
    }

    def get_code(key):
        if len(key) == 1 and ord(key) >= ord('a') and ord(key) <= ord('z'):
            return ord(key) - ord('a') + 0x41
        elif key in Keys.vk_codes:
            return Keys.vk_codes[key]
        return None

    def code_down(vk_code):
        return ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000 != 0
        
    def down(key):
        vk_code = Keys.get_code(key)
        return None if vk_code == None else Keys.code_down(vk_code)
    
    def all_down():
        keys = []
        for i in range(ord('a'), ord('z') + 1):
            if Keys.down(chr(i)):
                keys.append(chr(i))
        for name in Keys.vk_codes:
            if Keys.down(name):
                keys.append(name)
        return keys
    
class Screen():
    def ANSI(args):
        if args is str:
            return f"\x1b[{args}"   
        ansi = [f"\x1b[{arg}" for arg in args]
        return "".join(ansi)
    
    def clear():
        return Screen.ANSI(["2J", "H"])

    def show_cursor(show):
        return Screen.ANSI("?25" + ("h" if show == True else "l"))

    def move_cursor(line, column):
        return Screen.ANSI(f"{line};{column}H")
