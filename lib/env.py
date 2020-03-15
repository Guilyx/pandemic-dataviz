# -*- coding: utf-8 -*-

'''
@author: Erwin Lejeune <erwin.lejeune15@gmail.com>
@date: 2020-03-15
------------------------------
@brief : 2D Map building Class
'''

from random import random
from sys import stdout

from lib.node import State

class ColorsBook:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class World():
    def __init__(self, L = 100, H = 100, P = 0.3):
        self.L = L
        self.H = H

        # the world is represented by an array with one dimension
        self.w = [0 for i in range(L*H)] # initialise every tile to empty (0)

        # add walls in the first and last columns
        for i in range(H):
            self.w[i*L] = 1
            self.w[i*L+L-1] = 1
        
        # add walls in the first and last lines
        for j in range(L):
            self.w[j] = 1
            self.w[(H-1)*L + j] = 1

        for i in range(H):
            for j in range(L):
                # add a wall in this tile with probability P and provided that it is neither
                # the starting tile nor the goal tile 
                if random() < P and not (i == 1 and j == 1) and not (i == H-2 and j == L-2):
                    self.w[i*L+j] = 1
    
    def list_available_tiles(self):
        available_tiles = []
        for i in range(self.L*self.H):
            if self.w[i] == 0:
                available_tiles.append(i)
        return(available_tiles)

     # display the world
    def display(self):

        print('')
        carriage = 30 - self.L
        spaces = ' ' * carriage
        dashes = '-' * (carriage + int(self.L/2) - 1)
        stdout.write ("\033[;1m")
        stdout.write(dashes + "ENV" + dashes + "\n\n")
        stdout.write("\033[0;0m")
        for i in range(self.H):
            for j in range(self.L):
                tile = self.w[i * self.L + j]
                if (j == 0):
                    if carriage > 0:
                        stdout.write(spaces)
                if tile == State.FREE:
                    stdout.write('.')
                elif tile == State.WALL:
                    stdout.write (ColorsBook.BOLD)
                    stdout.write('█')
                    stdout.write(ColorsBook.ENDC)
                elif tile == State.HEALTHY:
                    stdout.write(ColorsBook.OKGREEN)
                    stdout.write('o')
                    stdout.write(ColorsBook.ENDC)
                elif tile == State.INFECTED:
                    stdout.write(ColorsBook.BOLD + ColorsBook.WARNING)
                    stdout.write('o')
                    stdout.write(ColorsBook.ENDC)
                elif tile == State.CURED:
                    stdout.write(ColorsBook.OKBLUE + ColorsBook.BOLD)
                    stdout.write('o')
                    stdout.write(ColorsBook.ENDC)


            print('')
        