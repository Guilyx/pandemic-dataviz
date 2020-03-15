# -*- coding: utf-8 -*-

'''
@author: Erwin Lejeune <erwin.lejeune15@gmail.com>
@date: 2020-03-15
------------------------------
@brief : 2D Map building Class
'''

from random import random
from sys import stdout

class World():
    def __init__(self, L, H, P):
        self.L = L
        self.H = H

        # the world is represented by an array with one dimension
        self.w = [0 for i in range(L*H)] # initialise every tile to empty (0)

        for pos in self.w:
            self.column = pos % L
            self.row = pos % H

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
                if (j == 0):
                    if carriage > 0:
                        stdout.write(spaces)
                if self.w[i * self.L + j] == 0:
                    stdout.write('.')
                elif self.w[i * self.L + j] == 1:
                    stdout.write ("\033[;1m" + "\033[1;31m" )
                    stdout.write('█')
                    stdout.write("\033[0;0m")

            print('')
        