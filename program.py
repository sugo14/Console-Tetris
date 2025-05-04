from console_board import ConsoleBoard
import time
from tui import Keys
""" from audio import Audio """
from tui import Screen
import threading

""" AUDIO = False """

board = ConsoleBoard()
last_time = time.perf_counter()
move_time = 1.2
timer = 0
paused = False

def update():
    """Updates the printed board."""

    board.print()

def move_down():
    """Updates the board by moving the block down."""

    global timer
    timer = 0
    board.move_down()
    update()

""" def play_audio():
    while True:
        Audio.compile("main_song").play() """

def reset():
    """Resets the board and starts a new game."""

    global board, last_time, timer, paused
    board = ConsoleBoard()
    last_time = time.perf_counter()
    timer = 0
    paused = False
    board.print_first()
    update()

if __name__ == "__main__":
    """ if AUDIO:
        thread = threading.Thread(target=play_audio)
        thread.start() """

    print(Screen.show_cursor(False))
    reset()

    while True:
        # this doesnt work
        if Keys.first_down('p'):
            paused = not paused
        if paused:
            last_time = time.perf_counter()
            continue
        if board.game_over():
            reset()

        curr_time = time.perf_counter()
        timer += curr_time - last_time
        last_time = curr_time
        
        Keys.update()
        if timer > move_time:
            move_down()
        if Keys.first_down('a'):
            board.move_left()
        if Keys.first_down('d'):
            board.move_right()
        if Keys.first_down('w'):
            board.rotate()
        if Keys.first_down('s'):
            move_down()
        if Keys.first_down(' '):
            board.drop_block()
        if Keys.first_down('r'):
            reset()
        if len(Keys.all_first_down()) > 0:
            update()
