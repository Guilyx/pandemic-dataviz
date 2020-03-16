# -*- coding: utf-8 -*-

'''
@author: Erwin Lejeune <erwin.lejeune15@gmail.com>
@date: 2020-03-15
------------------------------
@brief : 2D Map building Class
'''

from random import random
from sys import stdout
import os
import time
from lib.state import State
from lib.colors import ColorsBook

class World():
    def __init__(self, L = 100, H = 100, P = 0.3):
        self.L = L
        self.H = H

        # the world is represented by an array with one dimension
        self.pos_matrix = [State.FREE for i in range(L*H)] # initialise every tile to empty (0)

        # add walls in the first and last columns
        for i in range(H):
            self.pos_matrix[i*L] = State.WALL
            self.pos_matrix[i*L+L-1] = State.WALL
        
        # add walls in the first and last lines
        for j in range(L):
            self.pos_matrix[j] = State.WALL
            self.pos_matrix[(H-1)*L + j] = State.WALL

        for i in range(H):
            for j in range(L):
                # add a wall in this tile with probability P and provided that it is neither
                # the starting tile nor the goal tile 
                if random() < P and not (i == 1 and j == 1) and not (i == H-2 and j == L-2):
                    self.pos_matrix[i*L+j] = State.WALL
    
    def list_available_tiles(self):
        available_tiles = []
        for i in range(self.L*self.H):
            if self.pos_matrix[i] == State.FREE:
                available_tiles.append(i)
        return(available_tiles)

     # display the world
    def display(self):
        time.sleep(0.01)
        os.system('clear')
        print('')
        carriage = 30 - self.L
        spaces = ' ' * carriage
        dashes = '-' * (carriage + int(self.L/2) - 1)
        stdout.write ("\033[;1m")
        stdout.write(dashes + "ENV" + dashes + "\n\n")
        stdout.write("\033[0;0m")
        for i in range(self.H):
            for j in range(self.L):
                tile = self.pos_matrix[i * self.L + j]
                if (j == 0):
                    if carriage > 0:
                        stdout.write(spaces)
                if tile == State.FREE:
                    stdout.write('.')
                elif tile == State.WALL:
                    stdout.write (ColorsBook.BOLD)
                    stdout.write('█')
                    stdout.write(ColorsBook.ENDC)
                elif tile == State.UNAFFECTED:
                    stdout.write(ColorsBook.OKGREEN + ColorsBook.BOLD)
                    stdout.write('o')
                    stdout.write(ColorsBook.ENDC)
                elif tile == State.INFECTED:
                    stdout.write(ColorsBook.BOLD + ColorsBook.FAIL)
                    stdout.write('o')
                    stdout.write(ColorsBook.ENDC)
                elif tile == State.CURED:
                    stdout.write(ColorsBook.OKBLUE + ColorsBook.BOLD)
                    stdout.write('o')
                    stdout.write(ColorsBook.ENDC)


            print('')
        