from board import Board
from win_input import win_input
import time

board = Board()
last_time = time.time()
move_time = 1.2
timer = move_time

# disable cursor
print("\x1b[?25l")

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
    if timer > move_time:
        move_down()
    key_down = win_input()
    if key_down == 'a':
        board.move_left()
    if key_down == 'd':
        board.move_right()
    if key_down == 'w':
        board.rotate()
    if key_down == 's':
        move_down()
    if key_down == ' ':
        board.next_block()
    if key_down != None:
        update()
