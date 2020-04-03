# -*- coding: utf-8 -*-

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from lib.env import World
from lib.pandemic import Pandemic
import random

a_env = World(50, 10, 0.3)
max_pop = len(a_env.list_available_tiles())
pop = int(max_pop*0.7)
deathProbability = 0.5
recoverProbability = 0.3
infectedProbability = 0.8

plague = Pandemic(1000, pop, infectedProbability,
                  recoverProbability, deathProbability, a_env, 1)
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
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, -3, 0.1, 0.1, 0.1, env)
    assert(corona.population > 0)

def test_population_overflow():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, 999999, 0.1, 0.1, 0.1, env)
    assert(corona.population == len(env.initial_available))

def test_negative_initial_cases():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, -3, 0, 0, 0, env, -2)
    assert(corona.n_infected >= 0)

def test_negative_spreadrange():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, -3, 0, 0, 0, env, -2, -2)
    assert(corona.spreadRange == 0 or corona.spreadRange == 1)

def test_outofbounds_spreadrange():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, -3, 0, 0, 0, env, -2, 500)
    assert(corona.spreadRange == 0 or corona.spreadRange == 1)

def test_float_spreadrange():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, -3, 0, 0, 0, env, -2, 0.5)
    assert(corona.spreadRange == 0 or corona.spreadRange == 1)

def test_float_initial_cases():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, -3, 0, 0, 0, env, -2.9, 0.5)
    assert(isinstance(corona.n_infected, int) == True)

def test_float_population():
    env = World(50, 10, 0.3)
    corona = Pandemic(1000, 99.44, 0, 0, 0, env, 1, 1)
    assert(isinstance(corona.population, int) == True)

