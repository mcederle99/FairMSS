def available_actions(state, category):
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


def available_actions_old(state, category):
    if category == 0:
        if state[0] == 0:
            actions = [0, 5, 10, 15]
        elif state[0] < 5:
            actions = [0, 5, 10]
        elif state[0] == 5:
            actions = [-5, 0, 5, 10]
        elif state[0] < 10:
            actions = [-5, 0, 5]
        elif state[0] == 10:
            actions = [-10, -5, 0, 5]
        elif state[0] < 15:
            actions = [-10, -5, 0]
        else:
            actions = [-15, -10, -5, 0]
    elif category == 1:
        if state[0] == 0:
            actions = [0, 5, 10, 15, 20]
        elif state[0] < 5:
            actions = [0, 5, 10, 15]
        elif state[0] == 5:
            actions = [-5, 0, 5, 10, 15]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10]
        elif state[0] == 10:
            actions = [-10, -5, 0, 5, 10]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5]
        elif state[0] == 15:
            actions = [-15, -10, -5, 0, 5]
        elif state[0] < 20:
            actions = [-15, -10, -5, 0]
        else:
            actions = [-20, -15, -10, -5, 0]
    elif category == 2:
        if state[0] == 0:
            actions = [0, 5, 10, 15, 20, 25]
        elif state[0] < 5:
            actions = [0, 5, 10, 15, 20]
        elif state[0] == 5:
            actions = [-5, 0, 5, 10, 15, 20]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10, 15]
        elif state[0] == 10:
            actions = [-10, -5, 0, 5, 10, 15]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5, 10]
        elif state[0] == 15:
            actions = [-15, -10, -5, 0, 5, 10]
        elif state[0] < 20:
            actions = [-15, -10, -5, 0, 5]
        elif state[0] == 20:
            actions = [-20, -15, -10, -5, 0, 5]
        elif state[0] < 25:
            actions = [-20, -15, -10, -5, 0]
        else:
            actions = [-25, -20, -15, -10, -5, 0]
    elif category == 3:
        if state[0] < 5:
            actions = [0, 5, 10, 15, 20, 25, 30]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10, 15, 20, 25, 30]
        elif state[0] == 10:
            actions = [-10, -5, 0, 5, 10, 15, 20, 25, 30]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5, 10, 15, 20, 25]
        elif state[0] == 15:
            actions = [-15, -10, -5, 0, 5, 10, 15, 20, 25]
        elif state[0] < 20:
            actions = [-15, -10, -5, 0, 5, 10, 15, 20]
        elif state[0] == 20:
            actions = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
        elif state[0] < 25:
            actions = [-20, -15, -10, -5, 0, 5, 10, 15]
        elif state[0] == 25:
            actions = [-25, -20, -15, -10, -5, 0, 5, 10, 15]
        elif state[0] < 30:
            actions = [-25, -20, -15, -10, -5, 0, 5, 10]
        elif state[0] == 30:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10]
        elif state[0] <= 35:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5]
        else:
            actions = [-30, -25, -20, -15, -10, -5, 0]
    elif category == 4:
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
        elif state[0] == 30:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        elif state[0] <= 35:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
        elif state[0] <= 40:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20]
        elif state[0] <= 45:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15]
        elif state[0] <= 50:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10]
        elif state[0] <= 55:
            actions = [-30, -25, -20, -15, -10, -5, 0, 5]
        else:
            actions = [-30, -25, -20, -15, -10, -5, 0]
    else:
        actions = None

    return actions
