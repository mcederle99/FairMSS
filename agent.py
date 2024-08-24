import random
import numpy as np


np.random.seed(0)


def available_actions(state):
    if state[1] == 0:
        if state[0] < 5:
            actions = [0, 5, 10, 20, 30]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10, 20, 30]
        elif state[0] < 20:
            actions = [-10, -5, 0, 5, 10, 20, 30]
        elif state[0] < 30:
            actions = [-20, -10, -5, 0, 5, 10, 20, 30]
        elif state[0] < 45:
            actions = [-30, -20, -10, -5, 0, 5, 10, 20, 30]
        elif state[0] < 55:
            actions = [-30, -20, -10, -5, 0, 5, 10, 20]
        elif state[0] < 65:
            actions = [-30, -20, -10, -5, 0, 5, 10]
        elif state[0] < 70:
            actions = [-30, -20, -10, -5, 0, 5]
        else:
            actions = [-30, -20, -10, -5, 0]
    elif state[1] == 1:
        if state[0] == 0:
            actions = [0, 5, 10, 20]
        elif state[0] < 5:
            actions = [0, 5, 10]
        elif state[0] < 10:
            actions = [-5, 0, 5, 10]
        elif state[0] < 15:
            actions = [-10, -5, 0, 5]
        elif state[0] < 20:
            actions = [-10, -5, 0]
        else:
            actions = [-20, -10, -5, 0]
    else:
        if state[0] == 0:
            actions = [0, 5, 10]
        if state[0] < 5:
            actions = [0, 5, 10]
        elif state[0] < 10:
            actions = [-5, 0, 5]
        else:
            actions = [-10, -5, 0]

    return actions


class RebalancingAgent:
    def __init__(self, epsilon=1, epsilon_decay=0.99985, min_epsilon=0):
        self.learning_rate = 0.1
        self.discount_factor = 0.9  # 0.01
        self.q_table = {}
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def set_epsilon(self, value):
        self.epsilon = value

    def get_q_value(self, state, action):
        # binned_state = get_state_bin(state)
        key = ((state[0], state[1], state[2]), action)

        return self.q_table.get(key, 0)

    def update_q_table(self, state, action, reward, next_state):
        # binned_state = get_state_bin(state)
        # binned_next_state = get_state_bin(next_state)
        actions = available_actions(next_state)

        max_q_next = max(self.get_q_value(next_state, a) for a in actions)
        q_current = self.get_q_value(state, action)

        q_new = np.round(q_current + self.learning_rate * (reward + self.discount_factor * max_q_next - q_current), 1)
        self.q_table[((state[0], state[1], state[2]), action)] = q_new

    def print_q_table(self):
        for key, value in self.q_table.items():
            v = key[1]
            print(f"State-Action: {key[0]} {v}, Q-Value: {value}")

    def decide_action(self, state):
        # binned_state = get_state_bin(state)
        actions = available_actions(state)

        if random.random() < self.epsilon:
            return random.choice(actions)
        else:
            q_values = [self.get_q_value(state, action) for action in actions]
            action = actions[np.argmax(q_values)]

        return action

    def update_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
