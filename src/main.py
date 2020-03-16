import pandas
import sys
import random
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.env import World
from lib.pandemic import Pandemic
from lib.state import State

def main():
    env = World(10, 10, 0.2)
    env.display()

def pandemic():
    env = World(20, 20)
    max_pop = len(env.list_available_tiles())
    pop = int(max_pop*0.6)
    plague = Pandemic(100000, pop, 0.1, 0.1, 0.1, env)
    plague.world.display()
    plague.spread()
    plague.display()


if __name__ == "__main__":
    pandemic()