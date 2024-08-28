def available_actions(state):
    if state[1] == 0:
        if state[0] == 0:
            actions = [0, 5, 10, 15]
        elif state[0] < 5:
            actions = [0, 5, 10]
        elif state[0] < 10:
            actions = [-5, 0, 5]
        elif state[0] < 15:
            actions = [-10, -5, 0]
        else:
            actions = [-15, -10, -5, 0]
    elif state[1] == 1:
        if state[0] == 0:
            actions = [0, 5, 10, 15, 20]
        elif state[0] < 5:
            actions = [0, 5, 10, 15]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5]
        elif state[0] < 20:
            actions = [-15, -10, -5, 0]
        else:
            actions = [-20, -15, -10, -5, 0]
    elif state[1] == 2:
        if state[0] == 0:
            actions = [0, 5, 10, 15, 20, 25]
        elif state[0] < 5:
            actions = [0, 5, 10, 15, 20]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10, 15]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5, 10]
        elif state[0] < 20:
            actions = [-15, -10, -5, 0, 5]
        elif state[0] < 25:
            actions = [-20, -15, -10, -5, 0]
        else:
            actions = [-25, -20, -15, -10, -5, 0]
    elif state[1] == 3:
        if state[0] < 5:
            actions = [0, 5, 10, 15, 20, 25, 30]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10, 15, 20, 25, 30]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5, 10, 15, 20, 25]
        elif state[0] < 20:
            actions = [-15, -10, -5, 0, 5, 10, 15, 20]
        elif state[0] < 25:
            actions = [-20, -15, -10, -5, 0, 5, 10, 15]
        elif state[0] < 30:
            actions = [-25, -20, -15, -10, -5, 0, 5, 10]
        elif state[0] < 35:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5]
        else:
            actions = [-30, -25, -20, -15, -10, -5, 0]
    elif state[1] == 4:
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
            actions = [-25, -20, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        elif state[0] < 35:
            actions = [-30, -25, -20, -10, -5, 0, 5, 10, 15, 20, 25]
        elif state[0] < 40:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20]
        elif state[0] < 45:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15]
        elif state[0] < 50:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10]
        elif state[0] < 55:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5]
        else:
            actions = [-30, -25, -20, -15, -10, -5, 0]
    else:
        actions = None

    return actions
