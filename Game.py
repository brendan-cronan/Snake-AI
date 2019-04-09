import pygame
import sys
import time
import random
import math
from Snake import Snake
import copy



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
        self.reset()

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

        self.snake = Snake()
        self.food_pos = self.update_food_position()


    """
    Called from the main loop.
    Handles most of the main mechanics.
    """
    def step(self, dir):
        
        #    direction, input_recieved = self.handle_events();
        direction = dir;
        #   print(direction)
        
        if direction == 0:
            direction = [-1,0]
        
        if direction == 1:
            direction = [0,-1]
        
        if direction == 2:
            direction = [1,0]
        
        if direction == 3:
            direction = [0,1]
        
        
        #        if not input_recieved:
        #            return
        
        moved = self.snake.move(direction)
        
        if moved:
            self.reward = 1
        #   print("moved")
        #  if moved is None :
        #   print('You did not move')

        elif moved == "GAME_OVER":
            self.Game_Over = True
            self.game_over()
        
        
        grow_status = self.check_collisions(self.snake.head, [self.food_pos] )
        if grow_status:
            self.food_pos = self.update_food_position()
            self.score+=1
            self.reward=100
            self.snake.grow()
        
        #Check for collisions with the body of the snake.
        self_collision_status = self.check_collisions(self.snake.head, self.snake.tail[1::])
        
        if self_collision_status:
            self.Game_Over = True
            self.game_over()
        
        #      return self.reward, self.Game_Over, self.score
        
        return self.getObservation(self.snake.head), self.reward, self.Game_Over, self.score







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
    """
    def update_food_position(self):

        out = []
        for i in range(Game.BOARD_CELL_NUMBER):
            for j in range(Game.BOARD_CELL_NUMBER):
                out.append([i,j])

        out.remove(self.snake.head)
        for pos in self.snake.tail:
            if pos in out:
                out.remove(pos)

        return random.choice(out)

    """
    Does all of the drawing to the canvas.
    """
    def render(self):
        self.screen.fill(Game.BACKGROUND_COLOR)
        #draw food at location
        pygame.draw.rect(self.screen, Game.FOOD_COLOR, pygame.Rect(self.food_pos[0]*Game.SQUARE_SIZE, self.food_pos[1]*Game.SQUARE_SIZE, Game.SQUARE_SIZE, Game.SQUARE_SIZE))

        snake_coord_x = self.snake.head[0]*Game.SQUARE_SIZE
        snake_coord_y = self.snake.head[1]*Game.SQUARE_SIZE
        #draw snake
        pygame.draw.rect(self.screen, Game.HEAD_COLOR, pygame.Rect(snake_coord_x, snake_coord_y,Game.SQUARE_SIZE,Game.SQUARE_SIZE))

        #snake body
        for i in self.snake.tail:
            pygame.draw.rect(self.screen, Game.TAIL_COLOR, pygame.Rect(i[0]*Game.SQUARE_SIZE, i[1]*Game.SQUARE_SIZE,Game.SQUARE_SIZE-1,Game.SQUARE_SIZE-1))


        self.show_score()

        #updates canvas
        pygame.display.flip()




    def handle_events(self):
        input_recieved = False
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
                   input_recieved = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                   direction[0] = -1
                   direction[1] = 0
                   input_recieved = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                   direction[1] = -1
                   direction[0] = 0
                   input_recieved = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                   direction[1] = 1
                   direction[0] = 0
                   input_recieved = True
                if event.key == pygame.K_SPACE:
                    self.reset()
                if event.key == pygame.K_ESCAPE:
                   pygame.event.post(pygame.event.Event(pygame.QUIT))
        return direction,input_recieved



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
        # myFont = pygame.font.SysFont('monaco', 72)
        # GOsurf = myFont.render("Game Over", True, Game.red)
        # GOrect = GOsurf.get_rect()
        # GOrect.midtop = (320, 25)
        # self.screen.blit(GOsurf, GOrect)
        # self.show_score(0)
        pygame.display.flip()
        self.reset()


    def ortho_distance(self, pos1, pos2):
        if pos2 == 0 :
            return 0

        x1 = pos1[0]
        y1 = pos1[1]

        x2 = pos2[0]
        y2 = pos2[1]

        return max(x2 - x1, y2 - y1)




    directions = {
    "Right":        [1,0], # right
    "Left":         [-1,0], # left

    "Down":         [0,1], # down
    "Up":           [0,-1], # up

    "Down-Right":   [1,1], # down-right
    "Up-Right":     [1,-1], # up-right

    "Down-Left":    [-1,1], # down-left
    "Up-Left":      [-1,-1], # up-left
    }

    def observe_line(self, pos, direction, wall, food, body):

        position = copy.deepcopy(pos)
        position[0] += direction[0]
        position[1] += direction[1]


        if position == self.food_pos and food == 0:
            food = position

        if position in self.snake.tail and body == 0:
            body = position



        # this will be false in the event that it is inside the board
        boundary = self.snake.check_bounds(position, Game.BOARD_CELL_NUMBER)
        if not boundary:#if outside the bounds...
            wall = position
            return(wall, food, body)
        else:
            return self.observe_line(position, direction, wall, food, body)



    def getObservation(self, pos):
        position = copy.deepcopy(pos)

        wall = 0
        food = 0
        body = 0


        observation_list = []

        observation_list= [
        self.observe_line(position, Game.directions['Right'], wall, food, body ),
        self.observe_line(position, Game.directions['Left'], wall, food, body ),
        self.observe_line(position, Game.directions['Down'], wall, food, body ),
        self.observe_line(position, Game.directions['Up'], wall, food, body ),

        self.observe_line(position, Game.directions['Down-Right'], wall, food, body ),
        self.observe_line(position, Game.directions['Up-Right'], wall, food, body ),
        self.observe_line(position, Game.directions['Down-Left'], wall, food, body ),
        self.observe_line(position, Game.directions['Up-Left'], wall, food, body )
        ]

        observation_distance_list = []

        for items in observation_list:
            for i in items:
                temp = self.ortho_distance(self.snake.head, i)
                observation_distance_list.append(temp)
        return observation_distance_list
