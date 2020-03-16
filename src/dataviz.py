import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')  # Change backend ( segfault issue )
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import sys
import random
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.state import State
from lib.pandemic import Pandemic
from lib.env import World


def stack_chart():
    env = World(20, 20, 0.2)
    max_pop = len(env.list_available_tiles())
    pop = int(max_pop*0.8)

    deathProbability = 0.04
    recoverProbability = 0.2
    infectedProbability = 0.8

    epochs = 1000

    plague = Pandemic(epochs, pop, infectedProbability,
                      recoverProbability, deathProbability, env, 1)
    plague.spread()

    x = range(1, plague.hardstop+2)
    y = [plague.healthy, plague.cured, plague.infected, plague.dead]
    
    pal = ["#2ecc71", "#3498db", "#e74c3c", "#9b59b6"]
    
    for i in range(plague.hardstop+2):
        try:
            y = [plague.healthy[:i], plague.cured[:i], plague.infected[:i], plague.dead[:i]]          
            plt.stackplot(x[:i], y, labels=['Unaffected', 'Cured', 'Infected', 'Dead'], colors=pal, alpha=0.4)
            plague.displayWorldHistory(i)
            if i == 0:
                plt.legend(loc='upper left')
            plt.pause(0.01)
        except KeyboardInterrupt:
            print("Exiting cleanly...")
            sys.exit()
    
    plt.show()

if __name__ == "__main__":
    stack_chart()