import pygame
import sys
import time
import random
import math

BOARD_CELL_NUMBER = 10


class Snake:
    def __init__(self):
        self.head = [5,5]
        self.tail = []
        self.facing = [0,0]
        self.growing=False



    """
    Executes the movement for the snake.  Updates position and facing.
    Also makes checks for facing and boundaries.

    """
    def move(self, direction):
        if not check_facing(direction):
            out_of_bounds = check_bounds(self.get_position_from_current(direction), BOARD_CELL_NUMBER)
            if not out_of_bounds:
                _move_snake(direction)
        else:
            return False




    """
    get the position from the given position in the given direction
    """
    def get_position(self, position, direction):
        new_pos = [ position[0]+direction[0] , position[1]+direction[1] ]
        return new_pos
    """
    get the position from the current Snake position in the given direction
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
    This method takes a direction --> [-1,0]
    and sets the snake's position to the tile in this direction

    This PRIVATE method assumes that the position is valid and has gone through all checks.
    """
    def _move_snake(self, direction):


        self.tail.insert(0, list(self.head))

        self.head[0] += direction[0]
        self.head[1] += direction[1]




        self.facing = direction

        if not self.growing:
            self.tail.pop()
        else:
            self.growing = False


    """
    Call this function when the snake eats a fruit.
    """
    def grow(self):
        self.growing = True


    """
    return True if the direction is valid.
    return False if the direction is "backwards"
        or the same as the opposite of the old direction.
    """
    def check_facing(self, direction):
        opposite_dir = [self.facing[0]*-1, self.facing[1]*-1]
        return not direction == opposite_dir

    """
    Return True if the new_position collides with given list of points
    """
    def check_collisions(self, new_position, collision_positions):
        collisions = [ True for loc in collision_positions if new_position == loc ]
        for flag in collisions:
            if flag:
                return flag;
