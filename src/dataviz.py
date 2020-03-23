import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')  # Change backend ( segfault issue )
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import sys
from os import system
import time
import random
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.state import State
from lib.pandemic import Pandemic
from lib.env import World


def stack_chart():
    env = World(40, 20, 0.1)
    max_pop = len(env.list_available_tiles())
    pop = int(max_pop*0.1)

    deathProbability = 0.04
    recoverProbability = 0.3
    infectedProbability = 0.75

    epochs = 1000

    plague = Pandemic(epochs, pop, infectedProbability,
                      recoverProbability, deathProbability, env, 1)
    plague.spread()

    x = range(1, plague.hardstop+2)
    y = [plague.healthy, plague.cured, plague.infected, plague.dead]
    
    pal = ["#2ecc71", "#3498db", "#e74c3c", "#9b59b6"]

    try:
        for i in range(3):
            print("Simulation starting in " + str(3-i) + "...")
            time.sleep(1)
            system('clear')
    except KeyboardInterrupt:
        pass
    
    for i in range(plague.hardstop):
        try:
            y = [plague.healthy[:i], plague.cured[:i], plague.infected[:i], plague.dead[:i]]          
            plt.stackplot(x[:i], y, labels=['Unaffected', 'Cured', 'Infected', 'Dead'], colors=pal, alpha=0.4)
            plague.displayWorldHistory(i)
            if i == 0:
                plt.legend(loc='upper left')
            plt.pause(0.1)
        except KeyboardInterrupt:
            print("Exiting cleanly...")
            sys.exit()
    
    while(True):
        try:
            plt.show()
        except KeyboardInterrupt:
            print("Exiting cleanly...")
            sys.exit()

if __name__ == "__main__":
    stack_chart()