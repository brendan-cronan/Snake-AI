import pygame
import sys
import time
import random
import math
from Snake import Snake
import copy



class Game:

    #Number of cells on the board.
    #   Suggested to choose an even division of the SCREEN_SIZE but not required.
    BOARD_CELL_NUMBER = 10

    #Constant for PyGame to define size of screen.
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 200, 200

    #Constant used to reduce number of times performing this calculation
    SQUARE_SIZE = SCREEN_WIDTH/(BOARD_CELL_NUMBER+1)
    #Where the snake starts
    INITIAL_POSITION = [BOARD_CELL_NUMBER/2,BOARD_CELL_NUMBER/2]
    #initial Direction of snake.
    INITIAL_DIRECTION = "RIGHT"


    #Color definitions
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    purple = pygame.Color(255,0,255)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    brown = pygame.Color(165, 42, 42)

    #Defining constants for easy changing.
    BACKGROUND_COLOR = white
    FOOD_COLOR = red
    TAIL_COLOR = green
    HEAD_COLOR = purple



    #pygame init and call the reset method to start a new game
    def __init__(self):
        pygame.init()
        self.reset()

    """
    Method to start a new game.
    Initializes all the relevant variables
        allows the AI to start a new game without completely closing.
    """
    def reset(self):
        #initialize screen size and the caption with pygame
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)
        pygame.display.set_caption("Snake Game")

        #Score variable to train AI.
        self.score = 0
        #Flag to determine if it should continue iterating.
        self.Game_Over = False

        #initialize Snake class object to store relevant information
        self.snake = Snake()
        #Set food position to random available position.
        self.food_pos = self.update_food_position()


    """
    Called from the main loop.
    Handles most of the main mechanics.
    """
    def step(self, dir):
        #just to rename variable
        direction = dir;

        if direction == 0:# Left
            direction = [-1,0]

        if direction == 1:# Up
            direction = [0,-1]

        if direction == 2:# Right
            direction = [1,0]

        if direction == 3:# Down
            direction = [0,1]

        #Call Snake move method and get the flag returned.
        moved = self.snake.move(direction)

        #reward AI for moving to encourage survivability
        if moved:
            self.reward = 1
        #  if moved is None:  #Only applicable if we need this condition

        #recieved an out of bounds error
        elif moved == "GAME_OVER":
            self.Game_Over = True #set flag to true
            self.game_over() # call game over method to reset the game.


        #check if the snake has eaten the food using helper method and set a flag.
        grow_status = self.check_collisions(self.snake.head, [self.food_pos] )
        if grow_status:#if it has eaten.
            #update location of food to unoccupied location
            self.food_pos = self.update_food_position()
            #increase score to display
            self.score+=1
            #increase reward by 100 to indicate a more significant benefit than moving.
            self.reward=100
            #Call the snake grow method to make it increase tail by 1.
            self.snake.grow()

        #Check for collisions with the body of the snake.
        self_collision_status = self.check_collisions(self.snake.head, self.snake.tail[1::])

        #if it has collided with itself, Game over.
        if self_collision_status:
            self.Game_Over = True
            self.game_over()

        #      return self.reward, self.Game_Over, self.score
        #Call method for observation gathering at the end of each turn
        #   along with current game state.
        return self.getObservation(self.snake.head), self.reward, self.Game_Over, self.score



    """
    Changes the food postion to a new random space as long as nothing else is there.
    """
    def update_food_position(self):

        #array of positions to return
        out = []
        for i in range(Game.BOARD_CELL_NUMBER):#loop through game board
            for j in range(Game.BOARD_CELL_NUMBER):
                out.append([i,j]) #append every position possible
        #remove from valid positions the location of the head.
        out.remove(self.snake.head)
        #loop through tail and remove those as well.
        for pos in self.snake.tail:
            if pos in out:
                out.remove(pos)

        return random.choice(out) #return a random location from the valid positions

    """
    Does all of the drawing to the canvas.
    Called from main loop if rendering is desired.
    """
    def render(self):
        #set background
        self.screen.fill(Game.BACKGROUND_COLOR)

        #draw food at location
        pygame.draw.rect(self.screen, Game.FOOD_COLOR, pygame.Rect(self.food_pos[0]*Game.SQUARE_SIZE, self.food_pos[1]*Game.SQUARE_SIZE, Game.SQUARE_SIZE, Game.SQUARE_SIZE))


        #draw snake head at the location calculated by multiplying position by square size.
        pygame.draw.rect(self.screen, Game.HEAD_COLOR, pygame.Rect(self.snake.head[0]*Game.SQUARE_SIZE, self.snake.head[1]*Game.SQUARE_SIZE,Game.SQUARE_SIZE,Game.SQUARE_SIZE))

        #drawing each segment in snake body
        #   size-1 in order to see the squares individually.
        for i in self.snake.tail:
            pygame.draw.rect(self.screen, Game.TAIL_COLOR, pygame.Rect(i[0]*Game.SQUARE_SIZE, i[1]*Game.SQUARE_SIZE,Game.SQUARE_SIZE-1,Game.SQUARE_SIZE-1))

        #call method to write score on screen.
        self.show_score()

        #updates canvas
        pygame.display.flip()



    """
    Handles all user input, not used by AI.
    """
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


    """
    Return True if the new_position collides with given list of points
    Return nothing if no collisions
    Same as Snake Class'
    """
    def check_collisions(self, position, collision_positions):
        #list comprehension to make a True value if the provided position is equal to any value in loc.
        collisions = [ 1 for loc in collision_positions if new_position == loc ]
        if 1 in collisions:#loop through and return True if any 1 values are present
            return True


    """
    Display score in top right corner of the screen.
    Lots of pygame specific function calls and just writes to the screen.
    """
    def show_score(self,choice=1):
        SFont = pygame.font.SysFont('monaco', 32)
        Ssurf = SFont.render("Score  :  {0}".format(self.score), True, Game.black)
        Srect = Ssurf.get_rect()
        if choice == 1:
            Srect.midtop = (80, 10)
        else:
            Srect.midtop = (320, 100)
        self.screen.blit(Ssurf, Srect)

    """
    Just updates the screen and resets the game.
    """
    def game_over(self):
        # myFont = pygame.font.SysFont('monaco', 72)
        # GOsurf = myFont.render("Game Over", True, Game.red)
        # GOrect = GOsurf.get_rect()
        # GOrect.midtop = (320, 25)
        # self.screen.blit(GOsurf, GOrect)
        # self.show_score(0)
        pygame.display.flip()
        self.reset()


    """
    Helper method that gets the max x or y distance between two points
    """
    def ortho_distance(self, pos1, pos2):
        #Check if given point even is valid
        #pos1 is always valid b/c it is the snake's position
        if not pos2 == 0 :
            return max(pos2[0] - pos1[0], pos2[1] - pos1[1])
        else:
            return 0



    #dictionary for each of the 8 directions we let the AI see in and their unit vectors.
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

    """
    Recursive helper method to get Snake AI's "Sight" in just one line.
    takes position, direction, and the three values it will eventually return.
    Return:
        Location of each value:
            Wall, Food, Tail
        along the direction given.
    """
    def observe_line(self, pos, direction, wall, food, body):

        position = copy.deepcopy(pos)#ensure no funny business.

        #move one space in direction
        position[0] += direction[0]
        position[1] += direction[1]

        #only if food is unassigned and the current location has food on it...
        if position == self.food_pos and food == 0:
            food = position # set food value to current location

        #if the tail is in the current location and body is unassigned...
        if position in self.snake.tail and body == 0:
            body = position # set body value to current position



        # this will be false in the event that it is inside the board
        boundary = self.snake.check_bounds(position, Game.BOARD_CELL_NUMBER)
        if not boundary:#if outside the bounds...
            #Set wall value to current position
            wall = position
            #there are no more positions to check so return whatever values have been gathered
            return(wall, food, body)
        else:
            #There are more positions to check so recursively call to next pos.
            return self.observe_line(position, direction, wall, food, body)


    """
    Method called by the AI to "See"
    Return:
        List of values used by Nerual Network
    """
    def getObservation(self, pos):
        position = copy.deepcopy(pos)#no funny business.

        #initial values passed to each method call.
        wall = 0
        food = 0
        body = 0

        observation_list = []


        #call helper method for each of the 8 sight directions and put in list.
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

        #loop through observations and get the distance from snake head to the given locations of each value.
        for items in observation_list:
            for i in items:
                observation_distance_list.append(self.ortho_distance(self.snake.head, i))

        return observation_distance_list
