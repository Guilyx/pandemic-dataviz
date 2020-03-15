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
        

    # Get Neighbours
