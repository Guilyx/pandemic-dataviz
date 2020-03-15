'''
author : guilyx <erwin.lejeune15@gmail.com>
date : 15/03/2020
licence : MIT
brief : a node represent a person
'''

from lib.env import World, ColorsBook


class State():
    FREE = 0
    WALL = 1
    HEALTHY = 2
    INFECTED = 3
    CURED = 4

    ALLOWED_= [FREE, WALL, HEALTHY, INFECTED, CURED]


class Node():
    def __init__(self, state, position):

        self.state = state
        self.position = position

        if state in State.ALLOWED_:
            pass
        else:
            print(ColorsBook.WARNING +
                  "Careful, Node class built with wrong type for STATE variable" + ColorsBook.ENDC)
        

    # Get Neighbours
