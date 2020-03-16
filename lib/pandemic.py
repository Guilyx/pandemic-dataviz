# -*- coding: utf-8 -*-

'''
@author: Erwin Lejeune <erwin.lejeune15@gmail.com>
@date: 2020-03-15
------------------------------
@brief : Disease spreading class
'''

import random
from copy import deepcopy
from lib.node import Node
from lib.state import State
from lib.env import World
from lib.colors import ColorsBook


class Pandemic():
    def __init__(self, epochs, population, infectProb, healProb, deathProb, World, n_infected=1, spreadRange=1):
        self.epochs = epochs
        self.hardstop = 0
        self.spreadRange = spreadRange
        self.population = population
        self.infectProb = infectProb
        self.healProb = healProb
        self.deathProb = deathProb
        self.world = World

        self.worldHistory = []
        self.n_infected = n_infected

        self.nodes = dict()
        self.healthy = []
        self.cured = []
        self.infected = []
        self.dead = []

        free_tiles = World.list_available_tiles()
        free_tiles_n = len(free_tiles)
        if population > free_tiles_n:
            print(ColorsBook.WARNING +
                  "Careful, population higher than allocated space : forcing it at maximum" + ColorsBook.ENDC)
            self.population = free_tiles_n
        if epochs <= 0:
            print(ColorsBook.FAIL +
                  "Negative or Zero number of EPOCHS is not allowed, terminating..." + ColorsBook.ENDC)
            exit()
        if (infectProb or healProb or deathProb) < 0:
            print(ColorsBook.FAIL +
                  "Negative probabilities not allowed, terminating..." + ColorsBook.ENDC)
            exit()

        # Generates Nodes at random available spot
        for i in range(self.population):
            random.shuffle(free_tiles)
            picked_spot = free_tiles.pop()
            self.world.pos_matrix[picked_spot] = State.UNAFFECTED
            self.nodes[picked_spot] = Node(State.UNAFFECTED, picked_spot)

    def __getNumberState(self, state):
        numberState = 0
        for elem in list(self.nodes.keys()):
            if self.nodes[elem].state == state:
                numberState += 1
        return numberState

    def __updateStatisticsEpoch(self):
        self.dead.append(self.__getNumberState(State.DEAD))
        self.cured.append(self.__getNumberState(State.CURED))
        self.infected.append(self.__getNumberState(State.INFECTED))
        self.healthy.append(self.__getNumberState(State.UNAFFECTED))

    def displayStatisticsEpoch(self, epoch):
        if self.hardstop == 0:
            print(("\n- - - - " + ColorsBook.BOLD + "Epoch: {:d}/{:d}").format(
                epoch+1, self.epochs) + ColorsBook.ENDC)
        else:
            progress = epoch+1/self.hardstop*100
            progress = round(progress, 2)
            print(("\n- - - - " + ColorsBook.BOLD + "Progress: {:0.2f}%").format(
                progress, self.hardstop) + ColorsBook.ENDC)

        print(("- - - - " +
               ColorsBook.BOLD + ColorsBook.OKGREEN + "Unaffected: {:d}\t" + ColorsBook.ENDC +
               ColorsBook.BOLD + ColorsBook.OKBLUE + "Cured: {:d}\t" + ColorsBook.ENDC +
               ColorsBook.BOLD + ColorsBook.FAIL + "Infected: {:d}\t" + ColorsBook.ENDC +
               ColorsBook.HEADER + ColorsBook.BOLD + "Deaths: {:d}\t").format(
            self.healthy[epoch], self.cured[epoch], self.infected[epoch], self.dead[epoch]) + ColorsBook.ENDC)

    def __virusGrowth(self, Node):
        if not(Node.has_grown):
            Node.time_infected += 1
            Node.virus_gravity += Node.time_infected * random.random()
            Node.has_grown = True

    def __evolve(self):
        for elem in list(self.nodes.keys()):
            current_node = self.nodes[elem]
            node_state = current_node.state
            if node_state == State.DEAD:
                self.world.pos_matrix[elem] = State.FREE
            else:
                self.world.pos_matrix[elem] = node_state
            

    def __firstEpoch(self):
        people = list(self.nodes.keys())
        while self.__getNumberState(State.INFECTED) != self.n_infected:
            rdn_ = random.choice(people)
            self.nodes[rdn_].state = State.INFECTED

    def __genericEpoch(self):
        for elem in list(self.nodes.keys()):
            neighbours = self.nodes[elem].neighbours(
                self.spreadRange, self.world)
            if self.nodes[elem].state == State.INFECTED:

                # Put down the virus evolution flag
                self.nodes[elem].has_grown = False

                # Spread
                for elem in neighbours:
                    if self.nodes[elem].state == State.CURED:
                        spread_ = random.random()
                        if spread_ < self.infectProb/5:
                            self.nodes[elem].state = State.INFECTED
                    else:
                        spread_ = random.random()
                        if spread_ < self.infectProb:
                            self.nodes[elem].state = State.INFECTED

                # Death
                if self.nodes[elem].state == State.INFECTED:
                    if self.nodes[elem].virus_gravity > self.epochs * 0.3:
                        rdn_ = random.random()
                        if rdn_ < self.deathProb:
                            self.nodes[elem].state = State.DEAD
                    else:
                        rdn_ = random.random()
                        if rdn_ < self.deathProb/2:
                            self.nodes[elem].state = State.DEAD

                # Recovery
                cured_ = random.random()
                if cured_ < self.healProb and self.nodes[elem].state == State.INFECTED:
                    self.nodes[elem].state = State.CURED

                if self.nodes[elem].state == State.INFECTED:
                    self.__virusGrowth(self.nodes[elem])

    def displayTerminal(self, epoch):
        self.world.display()
        self.displayStatisticsEpoch(epoch)
    
    def displayWorldHistory(self, epoch):
        self.worldHistory[epoch].display()
        self.displayStatisticsEpoch(epoch)

    def spread(self, display=False):
        for i in range(self.epochs):
            if i == 0:
                self.__firstEpoch()
            else:
                self.__genericEpoch()

            self.__evolve()
            self.__updateStatisticsEpoch()

            if display:
                self.displayTerminal(i)

            world_ = deepcopy(self.world)
            self.worldHistory.append(world_)

            if (self.__getNumberState(State.INFECTED) == 0):
                print(ColorsBook.OKGREEN + ColorsBook.BOLD +
                      "\nCongrats, you survived the Pandemic in " + str(i) + " epochs !" + ColorsBook.ENDC)
                self.hardstop = i
                break
            if (self.__getNumberState(State.UNAFFECTED) + self.__getNumberState(State.CURED)) == 0:
                print(ColorsBook.FAIL + ColorsBook.BOLD +
                      "\nOops, the whole goddamn population has been decimated in " + str(i) + " epochs !" + ColorsBook.ENDC)
                self.hardstop = i
                break
