import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')  # or whatever other backend that you want
import matplotlib.pyplot as plt
import seaborn as sns
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


def stack_chart():
    env = World(20, 20)
    max_pop = len(env.list_available_tiles())
    pop = int(max_pop*0.6)

    deathProbability = 0.04
    recoverProbability = 0.2
    infectedProbability = 0.7

    epochs = 10000

    plague = Pandemic(epochs, pop, infectedProbability,
                      recoverProbability, deathProbability, env, 1)
    plague.spread(False)

    x = range(1, epochs+1)
    y = [plague.healthy, plague.cured, plague.infected, plague.dead]

    plt.stackplot(x, y, labels=['Unaffected', 'Cured', 'Infected', 'Dead'])
    plt.legend(loc='upper left')
    plt.show()


def pandemic():
    env = World(20, 20)
    max_pop = len(env.list_available_tiles())
    pop = int(max_pop*0.6)

    deathProbability = 0.04
    recoverProbability = 0.2
    infectedProbability = 0.7

    plague = Pandemic(100000, pop, infectedProbability,
                      recoverProbability, deathProbability, env, 1)
    plague.world.display()
    plague.spread()


if __name__ == "__main__":
    stack_chart()