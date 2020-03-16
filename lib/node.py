'''
author : guilyx <erwin.lejeune15@gmail.com>
date : 15/03/2020
licence : MIT
brief : a node represent a person
'''

from lib.env import World
from lib.colors import ColorsBook
from lib.state import State

class Node():
    def __init__(self, state, position):

        self.state = state
        self.position = position

        if state in State.ALLOWED_:
            pass
        else:
            print(ColorsBook.WARNING +
                  "Careful, Node class built with wrong type for STATE variable" + ColorsBook.ENDC)
        

    # Get Neighbours (degree : range)
    # range = 0 : direct neighbours, range = 1 : neighbours with diagonals etc...
    def neighbours(self, range_, World):
        i = self.position

        if i < 0 or i >= World.L * World.H or World.pos_matrix[i] == 1:
            # i is an incorrect tile number (outside the array or on a wall)
            return [] 

        if (range_ == 1) :
            successors = list(filter(lambda x: World.pos_matrix[x] != State.WALL, [i - 1, 
                                                                      i + 1, 
                                                                      i - World.L, 
                                                                      i + World.L, 
                                                                      i - World.L - 1, 
                                                                      i - World.L + 1, 
                                                                      i + World.L - 1, 
                                                                      i + World.L + 1]))
            return successors

        elif (range_ == 0):
            # look in the four adjacent tiles and keep only those with no wall
            successors = list(filter(lambda x: World.pos_matrix[x] != 1, [i - 1, 
                                                                      i + 1, 
                                                                      i - World.L, 
                                                                      i + World.L]))
            return successors
        
        else:
            print(ColorsBook.WARNING + "Range > 1 not yet implemented" + ColorsBook.ENDC)

        
