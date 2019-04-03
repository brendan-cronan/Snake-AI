import pygame
import sys
import time
import random
import math

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
    print(new_pos)
    return new_pos

"""
Updates the Snake's position.
input: [left/right direction, up/down direction]
with only acceptable values being
-1, 0, 1
for indicating the direction in which to move.
"""
def moveSnake(direction, current_pos):
    new_pos = [current_pos[0], current_pos[1]]
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
    pygame.draw.rect(playSurface, green, pygame.Rect(snake_coord_x, snake_coord_y,square_size,square_size))

    #updates canvas
    pygame.display.flip()




def handle_events():
    direction = [0,0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction[0] = 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction[0] = -1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                direction[1] = -1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction[1] = 1
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_SPACE:
                food_pos=updateFoodPosition()
    return direction


def check_collisions(new_position, collision_positions):
    collisions = [ True for loc in collision_positions if new_position == loc ]
    for i in collisions:
        if i:
            return i;



BOARD_CELL_NUMBER = 70

print(width)

square_size = width/(BOARD_CELL_NUMBER+1)

print(square_size)


snake_pos = [10,10]
direction = "RIGHT"

board = init_board(BOARD_CELL_NUMBER);
#print(board)
food_pos = updateFoodPosition()




while True:
    direction = handle_events()

    new_snake_pos = moveSnake(direction,snake_pos)
    if new_snake_pos == snake_pos:
        continue


    grow_status = check_collisions(new_snake_pos, [food_pos] )
    if (grow_status):
        print("COLLISION")

    snake_pos = new_snake_pos
    drawBoard();








def showScore(choice=1):
    SFont = pygame.font.SysFont('monaco', 32)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (320, 100)
    playSurface.blit(Ssurf, Srect)
