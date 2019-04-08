import pygame
import sys
import time
import random
import math
from Snake import Snake



class Game:

    BOARD_CELL_NUMBER = 10


    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 200, 200

    SQUARE_SIZE = SCREEN_WIDTH/(BOARD_CELL_NUMBER+1)
    INITIAL_POSITION = [BOARD_CELL_NUMBER/2,BOARD_CELL_NUMBER/2]
    INITIAL_DIRECTION = "RIGHT"


    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    purple = pygame.Color(255,0,255)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    brown = pygame.Color(165, 42, 42)


    BACKGROUND_COLOR = white
    FOOD_COLOR = red
    TAIL_COLOR = green
    HEAD_COLOR = purple




    def __init__(self):
        pygame.init()

    """
    Method to start a new game.
    """
    def reset(self):
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)
        pygame.display.set_caption("Snake Game")

        self.score = 0
        self.Game_Over = False
        self.board = self.init_board(Game.BOARD_CELL_NUMBER);
        #print(board)
        self.food_pos = self.updateFoodPosition()

        self.snake = Snake()







    """
    Sets up the board array and takes care of most initialization.
    """
    def init_board(self, cells):
        game_board = []
        for x in range(cells):
            lst = [ 0 for x in range(cells) ]
            game_board.append(lst)

        return game_board

    """
    Changes the food postion to a new random space.

    TODO: make sure it spawns in a free space.
    """
    def updateFoodPosition(self):
        new_pos = [random.randint(0,len(self.board)),random.randint(0,len(self.board)) ]
        # print(new_pos)
        return new_pos

    """
    Does all of the drawing to the canvas.
    """
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        #draw food at location
        pygame.draw.rect(self.screen, FOOD_COLOR, pygame.Rect(food_pos[0]*SQUARE_SIZE, food_pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        snake_coord_x = snake_pos[0]*SQUARE_SIZE
        snake_coord_y = snake_pos[1]*SQUARE_SIZE
        #draw snake
        pygame.draw.rect(self.screen, HEAD_COLOR, pygame.Rect(snake_coord_x, snake_coord_y,SQUARE_SIZE,SQUARE_SIZE))

        #snake body
        for i in snake_body:
            pygame.draw.rect(self.screen, TAIL_COLOR, pygame.Rect(i[0]*SQUARE_SIZE, i[1]*SQUARE_SIZE,SQUARE_SIZE-1,SQUARE_SIZE-1))


        show_score()

        #updates canvas
        pygame.display.flip()




    def handle_events(self):
        direction = [0,0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # direction[0] = random.randrange(-1,2)
                # print(direction[0])
                # direction[1] = random.randrange(-1,2)
                #print(direction[1])
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                   direction[0] = 1
                   direction[1] = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                   direction[0] = -1
                   direction[1] = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                   direction[1] = -1
                   direction[0] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                   direction[1] = 1
                   direction[0] = 0
                if event.key == pygame.K_ESCAPE:
                   pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_SPACE:
                   food_pos=updateFoodPosition()
                   #print("SPACE")
        return direction



    def check_collisions(self, position, collision_positions):
        collisions = [ True for loc in collision_positions if position == loc ]
        for flag in collisions:
            if flag:
                return flag;






    def show_score(self,choice=1):
        SFont = pygame.font.SysFont('monaco', 32)
        Ssurf = SFont.render("Score  :  {0}".format(self.score), True, Game.black)
        Srect = Ssurf.get_rect()
        if choice == 1:
            Srect.midtop = (80, 10)
        else:
            Srect.midtop = (320, 100)
        self.screen.blit(Ssurf, Srect)

    def game_over(self):
        myFont = pygame.font.SysFont('monaco', 72)
        GOsurf = myFont.render("Game Over", True, Game.red)
        GOrect = GOsurf.get_rect()
        GOrect.midtop = (320, 25)
        self.screen.blit(GOsurf, GOrect)
        self.show_score(0)
        pygame.display.flip()



    """
    Called from the main loop.
    Handles most of the main mechanics.
    """
    def step(self):
        direction = self.handle_events();

        moved = self.snake.move(direction)

        if not moved:
            print('You did not move')
        elif moved == "GAME_OVER":
            self.Game_Over = True
            self.game_over()

        grow_status = self.check_collisions(self.snake.head, [self.food_pos] )
        if grow_status:
            self.food_pos = self.updateFoodPosition()
            self.score+=1
            self.snake.grow()

        #Check for collisions with the body of the snake.
        self_collision_status = self.check_collisions(self.snake.head, self.snake.tail[1::])

        if self_collision_status:
            self.Game_Over = True
            self.game_over()

        if not self.Game_Over:
            self.drawBoard()
