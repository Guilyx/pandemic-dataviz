# -*- coding: utf-8 -*-

'''
@author: Erwin Lejeune <erwin.lejeune15@gmail.com>
@date: 2020-03-15
------------------------------
@brief : Disease spreading class
'''

import random
from lib.node import Node
from lib.state import State
from lib.env import World
from lib.colors import ColorsBook

class Pandemic():
    def __init__(self, epochs, population, infectProb, healProb, deathProb, World):
        self.epochs = epochs
        self.population = population
        self.infectProb = infectProb
        self.healProb = healProb
        self.deathProb = deathProb
        self.world = World
        self.nodes = dict()

        free_tiles = World.list_available_tiles()
        free_tiles_n = len(free_tiles)
        if population > free_tiles_n:
            print(ColorsBook.WARNING + "Careful, population higher than allocated space : forcing it at maximum" + ColorsBook.ENDC)
            self.population = free_tiles_n
        if epochs <= 0:
            print(ColorsBook.FAIL + "Negative or Zero number of EPOCHS is not allowed, terminating..." + ColorsBook.ENDC)
            exit()
        if (infectProb or healProb or deathProb) < 0:
            print(ColorsBook.FAIL + "Negative probabilities not allowed, terminating..." + ColorsBook.ENDC)
            exit()

        # Generates Nodes at random available spot
        for i in range(self.population):
            random.shuffle(free_tiles)
            picked_spot = free_tiles.pop()
            self.world.pos_matrix[picked_spot] = State.HEALTHY
            self.nodes[picked_spot] = Node(State.HEALTHY, picked_spot)

    def evolve(self):
        for elem in list(self.nodes.keys()):
            current_node = self.nodes[elem]
            node_state = current_node.state
            self.world.pos_matrix[elem] = node_state

    def spread(self):
        pass

        