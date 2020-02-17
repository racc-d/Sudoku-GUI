import pygame
import sys
import time
from create_random_solved_sudoku import generate_sudoku
from solver import create_hidden
import copy
import random

pygame.font.init()
pygame.init()

#main grid
grid = generate_sudoku()

#setting up permanent grid(Numbers that user won't be able to change)
permanent_grid = copy.deepcopy(grid)

#removing elements grid(Numbers that user won't be able to change)
permanent_grid = create_hidden(permanent_grid)

#setting up playing grid
playing_grid = copy.deepcopy(permanent_grid)

#Setting colors and backgrounds
black = (0, 0, 0)
white = (255, 255, 255)
perma_highlight = pygame.image.load("highlight.png").convert(8)
perma_highlight.set_alpha(75)
grid_highlight = pygame.image.load("play_grid_highlight.png").convert(8)
grid_highlight.set_alpha(255)
white_highlight = pygame.image.load("white.png").convert(8)
green = (0, 255, 0)
red = (255, 0, 0)

#setting fonts
win_font = pygame.font.SysFont("bahnschrift", 36, False, False)

#Setting the caption
pygame.display.set_caption("Sudoku By RS")

#Initialising the main_window
main_display = pygame.display.set_mode((540, 600)) #width, height

#Setting time counter
start = time.time()

#Setting main font
font = pygame.font.SysFont('arial', 16, bold=True)

#start time
start = time.time()

#valid keyboard inputs
keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6\
       ,pygame.K_7, pygame.K_8, pygame.K_9]

#Draw lines on the Grid
"""We will be using the bottom part of the window for 2 additional features, the
check answers button and the timer, so we will be restricting the actual Sudoku
grid to a smaller window, hence not the equal width and height when Initialising
the main window

Before drawing the lines for the grid, let's segregate the grid and the bottom
part, where we will insert our two features"""
pygame.draw.line(main_display, black, (0, 540), (540, 540), 2) #drawing the line

def draw_gridlines(): #Draw grid lines
    count = 60

    #Drawing minor lines
    for i in range(9):
        pygame.draw.line(main_display, black, (0, count), (540, count))
        pygame.draw.line(main_display, black, (count, 0), (count, 540))
        count += 60

    #Drawing major lines(subgrid)
    count = 180
    for i in range(3):
        pygame.draw.line(main_display, black, (count, 0), (count, 540), 3)
        pygame.draw.line(main_display, black, (0, count), (540, count), 3)
        count += 180

#change mouse co-ordinates to grid co-ordinates
def mouse_to_grid_pos(mouse_pos):
    grid_pos = (mouse_pos[1] // 60, mouse_pos[0] // 60)

    return grid_pos

#change mouse position to update position
def mouse_to_update_pos(mouse_pos):
    update_pos = copy.deepcopy(mouse_to_grid_pos(mouse_pos))
    update = ((update_pos[0] * 60) + 20, (update_pos[1] * 60) + 15)

    return update

#grid to update position
def grid_to_update(grid_pos):
    update_pos = ((grid_pos[1] * 60), (grid_pos[0] * 60))
    return update_pos

#not allow permanent positions to be changes
def is_perma(mouse_pos):
    grid_pos = mouse_to_grid_pos(mouse_pos)
    if permanent_grid[grid_pos[0]][grid_pos[1]] != 0:
        return True
    else:
        return False

#winning condition
def win():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != playing_grid[i][j]:
                return False
    return True

#check check answers
"""If user input is correct and the cell is not empty, show a green outline
outside the cell, otherwise show a red outline"""
def check_answers():
    for i in range(9):
        for j in range(9):
            update_pos = grid_to_update((i, j))
            if playing_grid[i][j] == grid[i][j] and playing_grid[i][j] != 0 and permanent_grid[i][j] == 0:
                pygame.draw.rect(main_display, green, \
                    (update_pos[0],update_pos[1], 60, 60), 2)
            if playing_grid[i][j] != grid[i][j] and playing_grid[i][j] != 0 and permanent_grid[i][j] == 0:
                pygame.draw.rect(main_display, red, \
                    (update_pos[0],update_pos[1], 60, 60), 2)

#update board
def update_board(grid_name):
    #populate grid with updated numbers
    update_font = pygame.font.SysFont("calibri", 36, True, False)
    for i in range(9):
        for j in range(9):
            if playing_grid[i][j] == permanent_grid[i][j]:
                continue
            else:
                message = update_font.render(str(playing_grid[i][j]), True, black)
                main_display.blit(message, (((j*60) + 20), (i*60) + 15))

    if check_ans:
        if not remove_check:
            check_answers()

#highlight permanent numbers
def highlight_perma(grid_name):
    const = 0
    for i in range(9):
        count = 0
        for j in range(9):
            if grid_name[i][j] != 0:
                main_display.blit(perma_highlight, (count, const))
                count += 60
            else:
                count += 60
        const += 60

    if check_ans:
        if not remove_check:
            check_answers()


#draw the check answer button
def create_check_answers():
    pygame.draw.rect(main_display, (255, 68, 68), (40, 550, 80, 40), 3)
    pygame.draw.rect(main_display, (171, 152, 152), (42, 552, 76, 36))

    check_font = pygame.font.SysFont("mistral", 28, False, False)

    message = check_font.render("CHECK", True, black)
    main_display.blit(message, (46, 558))

    if check_ans:
        if not remove_check:
            check_answers()


#draw the remove checks button
def create_remove_check_answers():
    pygame.draw.rect(main_display, (255, 68, 68), (160, 550, 120, 40), 3)
    pygame.draw.rect(main_display, (171, 152, 152), (162, 552, 116, 36))

    check_font = pygame.font.SysFont("mistral", 18, False, False)

    message = check_font.render("REMOVE CHECKS", True, black)
    main_display.blit(message, (166, 564))

    if check_ans:
        if not remove_check:
            check_answers()


#function to populate grid
def populate_grid(grid_name):
    const = 15
    num_font = pygame.font.SysFont("calibri", 36, True, False)
    for i in range(9):
        count = 20
        for j in range(9):
            if grid_name[i][j] != 0:
                message = num_font.render(str(grid_name[i][j]), True, black)
                main_display.blit(message, (count, const))
                count += 60
            else:
                count += 60
        const += 60

    if check_ans:
        if not remove_check:
            check_answers()


#update window after every event
def draw_window(time, grid_pos):
    # main_display.fill(white, (0, 0, 540, 540))
    for i in range(9):
        for j in range(9):
            update = grid_to_update((i,j))
            if i == grid_pos[0] and j == grid_pos[1] and permanent_grid[i][j] == 0:
                main_display.blit(grid_highlight, update)
            else:
                main_display.blit(white_highlight, update)

    main_display.fill((224, 224, 224), (0, 540, 540, 600))

    time_font = pygame.font.SysFont('calibri', 24, True)
    text = time_font.render("Time: " + format_time(time), True, black)

    main_display.blit(text, (420, 560))

    draw_gridlines()

    if check_ans:
        if not remove_check:
            check_answers()


#format time for counter
def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

#main game loop
check_ans = False
count = 1
while True:
    remove_check = False
    play_time = round(time.time() - start)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            save_mouse = pygame.mouse.get_pos()
            if 42 < save_mouse[0] < 42 + 76 and 552 < save_mouse[1] < 552 + 36:
                check_ans = True
            if 162 < save_mouse[0] < 162 + 116 and 552 < save_mouse[1] < 552 + 36:
                check_ans = False
        if event.type == pygame.MOUSEMOTION:
            # print('Detected mouse motion')
            save_mouse = pygame.mouse.get_pos()
            grid_pos = mouse_to_grid_pos(save_mouse)
        if event.type == pygame.KEYDOWN:
            if event.key in keys:
                pos = mouse_to_grid_pos(save_mouse)
                if is_perma(save_mouse):
                    pass
                else:
                    playing_grid[pos[0]][pos[1]] = keys.index(event.key) + 1
            elif event.key == pygame.K_BACKSPACE:
                try:
                    if playing_grid[pos[0]][pos[1]] != 0:
                        playing_grid[pos[0]][pos[1]] = 0
                    else:
                        continue
                except:
                    pass
    update_board(playing_grid)

    if not win():
        draw_window(play_time, grid_pos)

        highlight_perma(permanent_grid)

        populate_grid(permanent_grid)

        update_board(playing_grid)

        create_check_answers()

        create_remove_check_answers()

    if win():
        while count <= 1:
            update_board(playing_grid)
            count +=1
        pygame.draw.rect(main_display, (255, 68, 68), (2, 550, 364, 48), 3)
        pygame.draw.rect(main_display, (171, 152, 152), (4, 552, 360, 44))
        message = win_font.render("You Win!", True, (0, 0, 0))
        main_display.blit(message, (115, 550))

    pygame.display.flip()
