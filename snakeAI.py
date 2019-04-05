import pygame
import sys
import time
import random
import math

import gym
import numpy as np
import tflearn.layers.core import input_layer, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

LR = 1e-3
goal_steps = 300
score_requirement = 50
initial_games = 5000





#pygame init
init_status = pygame.init()
if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")


size = width, height = 700, 700
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")




red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
head = pygame.Color(255,0,255)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)


"""
Sets up the board array and takes care of most initialization.
"""
def init_board(cells):
    game_board = []
    for x in range(cells):
        lst = [ 0 for x in range(cells) ]
        game_board.append(lst)

    return game_board

"""
Changes the food postion to a new random space.

TODO: make sure it spawns in a free space.
"""
def updateFoodPosition():
    new_pos = [random.randint(0,len(board)),random.randint(0,len(board)) ]
    # print(new_pos)
    return new_pos

"""
Updates the Snake's position.
input: [left/right direction, up/down direction]
with only acceptable values being
-1, 0, 1
for indicating the direction in which to move.
"""
def moveSnake(facing, direction, current_pos):
    new_pos = [current_pos[0], current_pos[1]]

    opposite_dir = [facing[0]*-1, facing[1]*-1]
    # print(facing)

    if direction == opposite_dir:
        return new_pos

    #print(new_pos)
    new_pos[0] += direction[0]
    new_pos[1] += direction[1]
    #print(new_pos)
    return new_pos




"""
Does all of the drawing to the canvas.
"""
def drawBoard():
    playSurface.fill(white)

    #draw food at location
    pygame.draw.rect(playSurface, red, pygame.Rect(food_pos[0]*square_size, food_pos[1]*square_size, square_size, square_size))


    snake_coord_x = snake_pos[0]*square_size
    snake_coord_y = snake_pos[1]*square_size
    #draw snake
    pygame.draw.rect(playSurface, head, pygame.Rect(snake_coord_x, snake_coord_y,square_size,square_size))

    #snake body
    for i in snake_body:
        pygame.draw.rect(playSurface, green, pygame.Rect(i[0]*square_size, i[1]*square_size,square_size-1,square_size-1))


    show_score()

    #updates canvas
    pygame.display.flip()




def handle_events():
    direction = [0,0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
                #    elif event.type == pygame.KEYDOWN:
                direction[0] = random.randrange(-1,2)
                print(direction[0])
                direction[1] = random.randrange(-1,2)
                print(direction[1])
#            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
#                direction[0] = 1
#                direction[1] = 0
#            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
#                direction[0] = -1
#                direction[1] = 0
#            if event.key == pygame.K_UP or event.key == pygame.K_w:
#                direction[1] = -1
#                direction[0] = 0
#            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
#                direction[1] = 1
#                direction[0] = 0
#            if event.key == pygame.K_ESCAPE:
#                pygame.event.post(pygame.event.Event(pygame.QUIT))
#            if event.key == pygame.K_SPACE:
#                food_pos=updateFoodPosition()
#                print("SPACE")
    return direction


def check_collisions(new_position, collision_positions):
    collisions = [ True for loc in collision_positions if new_position == loc ]
    for i in collisions:
        if i:
            return i;

def check_bounds(new_position):
    if new_position[0] > BOARD_CELL_NUMBER or new_position[1] > BOARD_CELL_NUMBER or new_position[0] < 0 or new_position[1] < 0:
        return True



def show_score(choice=1):
    SFont = pygame.font.SysFont('monaco', 32)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (320, 100)
    playSurface.blit(Ssurf, Srect)

def game_over():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    playSurface.blit(GOsurf, GOrect)
    show_score(0)
    pygame.display.flip()



    #pygame.time.wait(5000)
    #pygame.quit()
    #sys.exit()





BOARD_CELL_NUMBER = 40

# print(width)

square_size = width/(BOARD_CELL_NUMBER+1)

# print(square_size)

score = 0
Game_Over = False

facing = [0,0]

snake_pos = [10,10]
snake_body = []
direction = "RIGHT"

board = init_board(BOARD_CELL_NUMBER);
#print(board)
food_pos = updateFoodPosition()




while True:
    direction = handle_events()



    new_snake_pos = moveSnake(facing, direction,snake_pos)

    #if you have moved...
    if new_snake_pos != snake_pos:

        facing = direction


        bounds_status = check_bounds(new_snake_pos)
        if bounds_status:
            # print("OUT OF BOUNDS")
            Game_Over=True
            game_over()

        snake_body.insert(0, list(snake_pos))

        grow_status = check_collisions(new_snake_pos, [food_pos] )
        if (grow_status):
            food_pos = updateFoodPosition()
            score+=1
        else:
            snake_body.pop()



        self_collision_status = check_collisions(new_snake_pos, snake_body[1::])

        if self_collision_status == True:
            Game_Over = True
            game_over()
            # print("BODY COLLISION")


        snake_pos = new_snake_pos

    #if game is still going
    if not Game_Over:
        drawBoard()
