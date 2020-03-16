import sys
import random
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.state import State
from lib.pandemic import Pandemic
from lib.env import World

def main():
    env = World(10, 10, 0.2)
    env.display()

def pandemic():
    env = World(20, 20, 0.1)
    max_pop = len(env.list_available_tiles())
    pop = int(max_pop*0.7)

    deathProbability = 0.04
    recoverProbability = 0.3
    infectedProbability = 0.7

    plague = Pandemic(1000, pop, infectedProbability,
                      recoverProbability, deathProbability, env, 1)
    plague.world.display()
    plague.spread()


if __name__ == "__main__":
    pandemic()