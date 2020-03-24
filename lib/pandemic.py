# -*- coding: utf-8 -*-

'''
@author: Erwin Lejeune <erwin.lejeune15@gmail.com>
@date: 2020-03-15
------------------------------
@brief : Disease spreading class
'''

import random
import sys
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
        self.has_spread = False

        self.nodes = dict()
        self.deaths_n = 0
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

        if population < 0:
            print(ColorsBook.WARNING +
                  "Careful, population can't be negative : forcing it at random number" + ColorsBook.ENDC)
            self.population = random.randint(1, free_tiles_n)

        if epochs <= 0:
            print(ColorsBook.FAIL +
                  "Negative or Zero number of EPOCHS is not allowed, terminating..." + ColorsBook.ENDC)
            sys.exit()
        if (infectProb or healProb or deathProb) < 0:
            print(ColorsBook.FAIL +
                  "Negative probabilities not allowed, terminating..." + ColorsBook.ENDC)
            sys.exit()

        if (spreadRange > 1):
            print(ColorsBook.WARNING +
                  "Careful, spreading range unsupported, forcing it at 1" + ColorsBook.ENDC)
            self.spreadRange = 1
        
        if (spreadRange < 0):
            print(ColorsBook.WARNING +
                  "Careful, spreading range unsupported, forcing it at 0" + ColorsBook.ENDC)
            self.spreadRange = 0

        if (n_infected < 0):
            print(ColorsBook.WARNING +
                  "Careful, initial number of infected can't be negative, forcing it at 1" + ColorsBook.ENDC)
            self.n_infected = 1
        
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
        self.dead.append(self.deaths_n)
        self.cured.append(self.__getNumberState(State.CURED))
        self.infected.append(self.__getNumberState(State.INFECTED))
        self.healthy.append(self.__getNumberState(State.UNAFFECTED))

    def displayStatisticsEpoch(self, epoch):
        if self.hardstop != 0:
            print(ColorsBook.BOLD + ("\n- - - -  Epoch: {:d}/{:d}").format(
                epoch+1, self.hardstop))
            progress = (epoch+1)/self.hardstop*100
            progress = round(progress, 2)

            print(
                ("\n- - - - " + "Initial Population: {:d}\t").format(self.population))

            print(("\n- - - - " + "Progress: {:0.2f}%").format(
                progress) + ColorsBook.ENDC)
        else:
            print(("\n- - - - " + ColorsBook.BOLD + "Epoch: {:d}/{:d}").format(
                epoch+1, self.epochs) + ColorsBook.ENDC)
            print(
                ("\n- - - - " + "Initial Population: {:d}\t").format(self.population))

            progress = (epoch+1)/self.epochs*100
            progress = round(progress, 2)

            print(("\n- - - - " + "Progress: {:0.2f}%").format(
                progress) + ColorsBook.ENDC)

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

    def __move(self):
        # move nodes to random neighbour available position
        free_neighbours = []
        previous_nodes = self.nodes
        for elem in list(self.nodes.keys()):
            if self.nodes[elem].state == State.DEAD or self.nodes[elem].state == State.FREE:
                pass
            else:
                should_move = random.random()
                if should_move < 0.2:
                    free_neighbours = self.nodes[elem].free_neighbours(
                        self.spreadRange, self.world)

                    if not free_neighbours:
                        pass
                    else:
                        picked_neighbour = random.choice(free_neighbours)
                        self.nodes[picked_neighbour] = self.nodes[elem]
                        self.world.pos_matrix[elem] = State.FREE
                        #self.world.pos_matrix[picked_neighbour] = self.nodes[elem].state
                        self.nodes.pop(elem)
                        self.__evolve()

        previous_len = len(list(previous_nodes.keys()))
        new_len = len(list(self.nodes.keys()))
        if previous_len != new_len:
            print("Program experienced Data Loss in number of nodes.")
            print("Loss : " + str(previous_len - new_len))

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
                for nigh in neighbours:
                    if self.nodes[nigh].state == State.CURED:
                        spread_ = random.random()
                        if spread_ < self.infectProb/5:
                            self.nodes[nigh].state = State.INFECTED
                    elif self.nodes[nigh].state == State.UNAFFECTED:
                        spread_ = random.random()
                        if spread_ < self.infectProb:
                            self.nodes[nigh].state = State.INFECTED

                # Death
                if self.nodes[elem].state == State.INFECTED:
                    if self.nodes[elem].virus_gravity > self.epochs * 0.3:
                        rdn_ = random.random()
                        if rdn_ < self.deathProb:
                            self.nodes[elem].state = State.DEAD
                            self.deaths_n += 1
                    else:
                        rdn_ = random.random()
                        if rdn_ < self.deathProb/2:
                            self.nodes[elem].state = State.DEAD
                            self.deaths_n += 1

                # Recovery
                cured_ = random.random()
                if cured_ < self.healProb and self.nodes[elem].state == State.INFECTED:
                    self.nodes[elem].state = State.CURED

                if self.nodes[elem].state == State.INFECTED:
                    self.__virusGrowth(self.nodes[elem])

                # At EACH epoch, the probability of finding a cure rises.
                # If cure is found : infection rate DRASTICALLY plummets.
                # To Do.

    def displayTerminal(self, epoch):
        self.world.display()
        self.displayStatisticsEpoch(epoch)

    def displayWorldHistory(self, epoch):
        self.worldHistory[epoch].display()
        self.displayStatisticsEpoch(epoch)

        if epoch+1 == self.hardstop:
            if (self.__getNumberState(State.INFECTED) == 0 and (self.__getNumberState(State.UNAFFECTED) + self.__getNumberState(State.CURED) != 0)):
                print(ColorsBook.OKGREEN + ColorsBook.BOLD +
                      "\nCongrats, you survived the Pandemic in " + str(self.hardstop) + " epochs !" + ColorsBook.ENDC)
            elif (self.__getNumberState(State.UNAFFECTED) + self.__getNumberState(State.CURED) + self.__getNumberState(State.INFECTED)) == 0:
                print(ColorsBook.FAIL + ColorsBook.BOLD +
                      "\nOops, the whole goddamn population has been decimated in " + str(self.hardstop) + " epochs !" + ColorsBook.ENDC)

    def spread(self, boolMove=True):
        for i in range(self.epochs+1):
            if boolMove:
                self.__move()
            if i == 0:
                self.__firstEpoch()
            else:
                self.__genericEpoch()

            self.__evolve()
            self.__updateStatisticsEpoch()

            world_ = deepcopy(self.world)
            self.worldHistory.append(world_)

            if (self.__getNumberState(State.INFECTED) == 0 and (self.__getNumberState(State.UNAFFECTED) + self.__getNumberState(State.CURED) != 0)):
                self.hardstop = i+1
                break
            elif (self.__getNumberState(State.UNAFFECTED) + self.__getNumberState(State.CURED) + self.__getNumberState(State.INFECTED)) == 0:
                self.hardstop = i+1
                break

            if (self.dead[i] + self.cured[i] + self.healthy[i] + self.infected[i] != self.population):
                print(ColorsBook.BOLD + ColorsBook.FAIL + "FAILURE : Number of nodes unmatched with initial population !!")

        if self.hardstop == 0:
            self.hardstop = self.epochs

        self.has_spread = True

    def show(self, boolMove):
        if self.has_spread:
            pass
        else:
            self.spread(boolMove)
        for i in range(self.hardstop):
            self.displayWorldHistory(i)
