class State():
    # Env States 
    FREE = 0
    WALL = 1

    # Node States
    UNAFFECTED = 2
    INFECTED = 3
    CURED = 4
    DEAD = 5

    ALLOWED_= [FREE, WALL, UNAFFECTED, INFECTED, CURED, DEAD]

