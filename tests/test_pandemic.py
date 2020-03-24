# -*- coding: utf-8 -*-

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from lib.env import World
from lib.pandemic import Pandemic
import random

env = World(50, 10, 0.3)
max_pop = len(env.list_available_tiles())
pop = int(max_pop*0.7)
deathProbability = 0.5
recoverProbability = 0.3
infectedProbability = 0.8

plague = Pandemic(1000, pop, infectedProbability,
                  recoverProbability, deathProbability, env, 1)
plague.spread()

def test_population_consistancy():
    if plague.hardstop != 0:
        loop = plague.hardstop
    else:
        loop = plague.epochs
    
    for i in range(loop):
        assumed_pop = plague.dead[i] + plague.cured[i] + plague.healthy[i] + plague.infected[i] 
        assert(assumed_pop == plague.population)

def test_negative_population():
    corona = Pandemic(1000, -3, 0.1, 0.1, 0.1, env)
    assert(corona.population > 0)

def test_population_overflow():
    corona = Pandemic(1000, 9999999999999999999999, 0.1, 0.1, 0.1, env)
    assert(corona.population == len(env.list_available_tiles()))

def test_negative_initial_cases():
    corona = Pandemic(1000, -3)


# test negative probabilities
# test negative number of initial cases
# test negative spreadRange
# test unsupported spreadRange