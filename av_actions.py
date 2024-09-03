def available_actions(state):
    if state[0] < 5:
        actions = [0, 5, 10, 15, 20, 25, 30]
    elif state[0] < 10:
        actions = [-5, 0, 5, 10, 15, 20, 25, 30]
    elif state[0] < 15:
        actions = [-10, -5, 0, 5, 10, 15, 20, 25, 30]
    elif state[0] < 20:
        actions = [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    elif state[0] < 25:
        actions = [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    elif state[0] < 30:
        actions = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    elif state[0] <= 70:
        actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    elif state[0] <= 75:
        actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
    elif state[0] <= 80:
        actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20]
    elif state[0] <= 85:
        actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15]
    elif state[0] <= 90:
        actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10]
    elif state[0] <= 95:
        actions = [-30, -25, -20, -15, -10, -5, 0, 5]
    else:
        actions = [-30, -25, -20, -15, -10, -5, 0]

    return actions
