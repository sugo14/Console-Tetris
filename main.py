from board import Board
import time
from tui import Keys, Screen

board = Board()
last_time = time.time()
move_time = 1.2
timer = move_time

Screen.show_cursor(False)

def update():
    board.print()

def move_down():
    global timer
    timer = 0
    update()
    board.move_down()

while True:
    curr_time = time.time()
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
        board.next_block()
    if len(Keys.all_first_down()) > 0:
        update()
