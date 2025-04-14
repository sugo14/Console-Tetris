from board import Board
import time
from tui import Keys, Screen

board = Board()
last_time = time.perf_counter()
move_time = 1.2
timer = 0

Screen.show_cursor(False)

def update():
    board.print()
    print(board.find_filled_rows())

def move_down():
    global timer
    timer = 0
    if board.block_grounded():
        board.drop_block()
    else:
        board.move_down()
    update()

update()
while True:
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
    if len(Keys.all_first_down()) > 0:
        update()
