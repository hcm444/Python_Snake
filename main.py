import PySimpleGUI as sg
from time import time
from random import randint


def convert_pos_to_pixel(cell):
    tl = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
    br = tl[0] + CELL_SIZE, tl[1] + CELL_SIZE
    return tl, br


def place_apple():
    food_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    while food_pos in snake_body:
        food_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    return food_pos


# game constants
FIELD_SIZE = 400
CELL_NUM = 30
CELL_SIZE = FIELD_SIZE / CELL_NUM

# snake
snake_body = [(4, 4), (3, 4), (2, 4)]
DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, 1), 'down': (0, -1)}
direction = DIRECTIONS['up']

# apple
apple_pos = place_apple()
apple_eaten = False
score =[sg.Text("Game")]
sg.theme('Dark2')
field = sg.Graph(
    canvas_size=(FIELD_SIZE, FIELD_SIZE),
    graph_bottom_left=(0, 0),
    graph_top_right=(FIELD_SIZE, FIELD_SIZE),
    background_color='black')
layout = [[score],[field]]

window = sg.Window('Snake', layout, return_keyboard_events=True)

start_time = time()
while True:
    event, values = window.read(timeout=0.5)
    if event == sg.WIN_CLOSED: break
    if event == 'a': direction = DIRECTIONS['left']
    if event == 'w': direction = DIRECTIONS['up']
    if event == 'd': direction = DIRECTIONS['right']
    if event == 's': direction = DIRECTIONS['down']

    time_since_start = time() - start_time
    if time_since_start >= 0.25:
        start_time = time()

        # apple snake collision
        if snake_body[0] == apple_pos:
            apple_pos = place_apple()
            apple_eaten = True

        # snake update
        new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
        snake_body.insert(0, new_head)
        if apple_eaten:
            pass
        else:
            snake_body.pop()
        apple_eaten = False

        if 0 <= snake_body[0][0] <= CELL_NUM - 1 and 0 <= snake_body[0][1] <= CELL_NUM - 1:
            if snake_body[0] in snake_body[1:]:
                break

            else:
                pass
        else:
            break
        score = [sg.Text(snake_body)]
        field.DrawRectangle((0, 0), (FIELD_SIZE, FIELD_SIZE), 'black')

        tl, br = convert_pos_to_pixel(apple_pos)
        field.DrawRectangle(tl, br, 'green')
        # draw snake
        for index, part in enumerate(snake_body):
            tl, br = convert_pos_to_pixel(part)
            if index == 0:
                color = 'green'
            else:
                color = 'yellow'
            field.DrawRectangle(tl, br, color)

window.close()
