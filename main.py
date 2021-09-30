import tkinter as tk
import random as rand
import tkinter.messagebox as tkm

# const variables
BOARD_SIZE = 8
NONE = 0
SET = 1
PLAYER = 0
COM = 1
BLACK = 1
WHITE = 2
FNT_SMALL = ('Times New Roman', 30)
FNT_LARGE = ('Times New Roman', 80)

# variables
cursor_row = 0
cursor_column = 0
flag = NONE
turn = PLAYER
phase = 0
msg = ''
space = 0

# lists
board = []
board_memory = []
for index in range(BOARD_SIZE):
    board.append([0] * BOARD_SIZE)
    board_memory.append([0] * BOARD_SIZE)

process = {
    'title': 0,
    'show_turn': 1,
    'place_stone': 2,
    'change_turn': 3,
    'search_placeable': 4,
    'judge_winner': 5
}

color = [0] * 2

who = ['You', 'Computer']


def main():
    global flag, phase, turn, msg, space
    draw_board()
    if phase == process['title']:
        msg = 'Choose playing first or second'
        cvs.create_text(320, 200, text='Othello', fill='gold', font=FNT_LARGE)
        cvs.create_text(160, 440, text='First (Black)', fill='lime', font=FNT_SMALL)
        cvs.create_text(480, 440, text='Second (White)', fill='lime', font=FNT_SMALL)
        if flag == SET:
            flag = NONE
            if cursor_row == 5 and 0 <= cursor_column <= 3:
                init_board()
                color[PLAYER] = BLACK
                color[COM] = WHITE
                turn = 0
                phase = process['show_turn']
            elif cursor_row == 5 and 4 <= cursor_column <= 7:
                init_board()
                color[PLAYER] = WHITE
                color[COM] = BLACK
                turn = 1
                phase = process['show_turn']

    elif phase == process['show_turn']:
        msg = 'Your turn'
        if turn == COM:
            msg = 'Computer is thinking'
        phase = process['place_stone']

    elif phase == process['place_stone']:
        if turn == PLAYER:
            if flag == SET:
                flag = NONE
                if count_placeable(cursor_row, cursor_column, color[turn]) > NONE:
                    place_stone(cursor_row, cursor_column, color[turn])
                    space -= 1
                    phase = process['change_turn']
        elif turn == COM:
            trial = [300, 300, 240, 180, 120, 60, 1]
            row, column = com_ai(color[turn], trial[int(space / 10)])
            place_stone(row, column, color[turn])
            space -= 1
            phase = process['change_turn']

    elif phase == process['change_turn']:
        msg = ''
        turn ^= 1
        phase = process['search_placeable']

    elif phase == process['search_placeable']:
        if space == 0:
            phase = process['judge_winner']
        elif not judge_placeable(BLACK) and not judge_placeable(WHITE):
            tkm.showinfo('', 'Finished')
            phase = process['judge_winner']
        elif not judge_placeable(color[turn]):
            tkm.showinfo('', f'{who[turn]} passed')
            phase = process['change_turn']
        else:
            phase = process['show_turn']

    elif phase == process['judge_winner']:
        black_stone, white_stone = count_stone()
        tkm.showinfo('Finished', f'Black={black_stone}, White={white_stone}')
        if black_stone == white_stone:
            tkm.showinfo('', 'Draw')
        elif (color[PLAYER] == BLACK and black_stone > white_stone) \
                or (color[PLAYER] == WHITE and white_stone > black_stone):
            tkm.showinfo('', 'You win!')
        else:
            tkm.showinfo('', 'Computer win!')
        phase = process['title']
    root.after(100, main)


def com_ai(com_color, loop):
    global msg
    win_cell_counter = [0] * (BOARD_SIZE ** 2)
    save_board()
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if count_placeable(row, column, com_color) > 0:
                msg += '.'
                draw_board()
                win_cell_counter[column + (row * BOARD_SIZE)] = 1
                for count in range(loop):
                    place_stone(row, column, com_color)
                    simulate_match(com_color)
                    black_stone, white_stone = count_stone()
                    if com_color == BLACK and black_stone > white_stone:
                        win_cell_counter[column + (row * BOARD_SIZE)] += 1
                    elif com_color == WHITE and white_stone > black_stone:
                        win_cell_counter[column + (row * BOARD_SIZE)] += 1
                    load_board()
    maximum = 0
    number = 0
    for i in range(BOARD_SIZE ** 2):
        if win_cell_counter[i] > maximum:
            maximum = win_cell_counter[i]
            number = i
    row = int(number / 8)
    column = number % 8

    return row, column


def save_board():
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            board_memory[row][column] = board[row][column]


def load_board():
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            board[row][column] = board_memory[row][column]


def simulate_match(com_color):
    while True:
        if not judge_placeable(BLACK) and not judge_placeable(WHITE):
            break

        com_color = 3 - com_color

        if judge_placeable(com_color):
            while True:
                row = rand.randint(0, BOARD_SIZE - 1)
                column = rand.randint(0, BOARD_SIZE - 1)
                if count_placeable(row, column, com_color) > 0:
                    place_stone(row, column, com_color)
                    break


def click_board(e):
    global cursor_row, cursor_column, flag
    flag = SET
    cursor_row = int(e.y/80)
    cursor_column = int(e.x/80)
    if cursor_row > 7:
        cursor_row = 7
    if cursor_column > 7:
        cursor_column = 7


def place_stone(row, column, turn_color):
    board[row][column] = turn_color
    for direction_y in range(-1, 2):
        for direction_x in range(-1, 2):
            count = 0
            relative_y = row
            relative_x = column
            while True:
                relative_y += direction_y
                relative_x += direction_x
                if relative_y < 0 or 7 < relative_y or relative_x < 0 or 7 < relative_x:
                    break
                if board[relative_y][relative_x] == NONE:
                    break
                if board[relative_y][relative_x] == (3 - turn_color):
                    count += 1
                if board[relative_y][relative_x] == turn_color:
                    for i in range(count):
                        relative_y -= direction_y
                        relative_x -= direction_x
                        board[relative_y][relative_x] = turn_color
                    break


def draw_board():
    cvs.delete('all')
    cvs.create_text(320, 670, text=msg, fill='silver', font=FNT_SMALL)
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            x = column * 80
            y = row * 80
            cvs.create_rectangle(x, y, x + 80, y + 80, outline='black')
            if board[row][column] == BLACK:
                cvs.create_oval(x + 10, y + 10, x + 70, y + 70, fill='black', width=0)
            if board[row][column] == WHITE:
                cvs.create_oval(x + 10, y + 10, x + 70, y + 70, fill='white', width=0)
            if count_placeable(row, column, color[turn]) > NONE:
                cvs.create_oval(x + 5, y + 5, x + 75, y + 75, outline='cyan', width=2)
    cvs.update()


def count_placeable(row, column, turn_color):
    if board[row][column] > NONE:
        return -1
    total = 0
    for direction_y in range(-1, 2):
        for direction_x in range(-1, 2):
            count = 0
            relative_y = row
            relative_x = column
            while True:
                relative_y += direction_y
                relative_x += direction_x
                if relative_y < 0 or 7 < relative_y or relative_x < 0 or 7 < relative_x:
                    break
                if board[relative_y][relative_x] == NONE:
                    break
                if board[relative_y][relative_x] == (3 - turn_color):
                    count += 1
                if board[relative_y][relative_x] == turn_color:
                    total += count
                    break
    return total


def count_stone():
    black = NONE
    white = NONE
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == BLACK:
                black += 1
            if board[row][column] == WHITE:
                white += 1
    return black, white


def judge_placeable(turn_color):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if count_placeable(row, column, turn_color) > NONE:
                return True
    return False


def init_board():
    global space
    space = (BOARD_SIZE ** 2) - 4
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            board[row][column] = 0
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[3][3] = WHITE
    board[4][4] = WHITE


root = tk.Tk()
root.title('Othello')
root.resizable(False, False)
root.bind('<Button>', click_board)
cvs = tk.Canvas(width=640, height=700, bg='green')
cvs.pack()
root.after(100, main)
root.mainloop()
