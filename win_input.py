import msvcrt

def win_input():
    """Recieves non-blocking character input from the console, including special characters. Only works on Windows.

    Raises:
        RuntimeError: Thrown when a non-arrow-key special character is inputted.

    Returns:
        str: The inputted key, or None if no key was pressed.
    """

    if not msvcrt.kbhit():
        return None
    byte = msvcrt.getch()

    # Arrow key magic
    if byte == b'\xe0':
        byte2 = msvcrt.getch()
        if byte2 == b'K':
            return 'left'
        elif byte2 == b'M':
            return 'right'
        elif byte2 == b'H':
            return 'up'
        elif byte2 == b'P':
            return 'down'
        else:
            # TODO: probably remove this
            raise RuntimeError("Bad special key pressed.")
        
    # Regular keys
    return byte.decode('utf-8')
