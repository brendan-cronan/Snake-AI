import pygame
import sys
import time
import random
import math

BOARD_CELL_NUMBER = 10


class Snake:
    """
    Initializes the important variables in the constructor
    """
    def __init__(self):
        #location of the head of the snake.  Starts at the middle.
        self.head = [BOARD_CELL_NUMBER/2,BOARD_CELL_NUMBER/2]
        #List of locations that it has occupied in the last [length] turns.
        self.tail = []
        #List of its *most recent* direction to avoid going "backwards"
        self.facing = [0,0]
        #boolean flag to determine whether to remove a value from self.tail
        self.growing=False



    """
    Executes the movement for the snake.  Updates position and facing.
    Also makes checks for facing and boundaries.
    Return True if any movement was made.
    Return "GAME_OVER" if the movement is out of bounds
    """
    def move(self, direction):
        #Call helper method to check that move is not trying to go backwards
        if self.check_facing(direction):#if not going backwards...
            #Method call to check if position in desired direction falls outside game bounds
            inside_bounds = self.check_bounds(self.get_position_from_current(direction), BOARD_CELL_NUMBER)
            if inside_bounds:#if inside the game bounds...
                self._move_snake(direction)#call private helper method to execute movement.
                return True#return true to indicates successful move
            else:
                return "GAME_OVER"#Only return Game over if it is out of bounds.
            #if it is merely trying to go backwards, return nothing.




    """
    Get a new position from the given location in the given direction
    """
    def get_position(self, position, direction):
        #merely returns the position with the direction added to it.
        return [ position[0]+direction[0] , position[1]+direction[1] ]

    """
    Get the position from the Current Snake Position in the given direction
    Just calls the get_position with the current location for convenience.
    """
    def get_position_from_current(self, direction):
        return self.get_position(self.head,direction)


    """
    Return True if valid position on board.
    Return False if it is outside the bounds or negative.
    """
    def check_bounds(self, new_position, bound):
        if new_position[0] > bound or new_position[1] > bound or new_position[0] < 0 or new_position[1] < 0:
            return False
        else:
            return True



    """
    This method takes a direction ex. --> [-1,0]
    and sets the snake's position to the tile in this direction

    This PRIVATE method assumes that the position is valid and has gone through all checks.
    """
    def _move_snake(self, direction):


        #add position to the tail before the movement.
        self.tail.insert(0, list(self.head))

        #actually change the position of the head
        self.head[0] += direction[0]
        self.head[1] += direction[1]

        #Set the facing to the "last" direction
        self.facing = direction

        #only pop off the last position in tail if it hasn't eaten this cycle.
        if not self.growing:
            self.tail.pop()
        else:#merely set the flag back to false to "grow"
            self.growing = False


    """
    Call this function when the snake eats a fruit.
    Called by the Game class.
    """
    def grow(self):
        self.growing = True


    """
    return True if the direction is valid.
    return False if the direction is "backwards"
        or the same as the opposite of the old direction.
    """
    def check_facing(self, direction):
        #opposite direction of the current facing is not allowed.
        opposite_dir = [self.facing[0]*-1, self.facing[1]*-1]
        return not direction == opposite_dir

    """
    Return True if the new_position collides with given list of points
    Return nothing if no collisions
    """
    def check_collisions(self, new_position, collision_positions):
        #list comprehension to make a True value if the provided position is equal to any value in loc.
        collisions = [ 1 for loc in collision_positions if new_position == loc ]
        if 1 in collisions:#loop through and return True if any 1 values are present
            return True
