import random
import numpy as np
from av_actions import available_actions


# np.random.seed(0)


class RebalancingAgent:
    def __init__(self, category, epsilon=1, epsilon_decay=8.25e-7, min_epsilon=0.01):
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.q_table = {}
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.category = category

    def set_epsilon(self, value):
        self.epsilon = value

    def get_q_value(self, state, action):
        key = ((state[0], state[1]), action)

        return self.q_table.get(key, 0)

    def update_q_table(self, state, action, reward, next_state):
        actions = available_actions(next_state, self.category)

        max_q_next = max(self.get_q_value(next_state, a) for a in actions)
        q_current = self.get_q_value(state, action)

        q_new = q_current + self.learning_rate * (reward + self.discount_factor * max_q_next - q_current)
        self.q_table[((state[0], state[1]), action)] = q_new

    def print_q_table(self):
        already_printed_states = []
        actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        for key in self.q_table.keys():
            values = []
            for a in actions:
                values.append(self.q_table.get((key[0], a), -1000))
            best_action = actions[np.argmax(values)]
            if best_action < 0:
                if key[0] not in already_printed_states:
                    print(f"State-Action: {key[0]} {best_action}")
                    for a in actions:
                        print(self.q_table.get((key[0], a), -1000))
                    already_printed_states.append(key[0])
                    print('----------------------')

    def decide_action(self, state):
        actions = available_actions(state, self.category)

        if random.random() < self.epsilon:
            return random.choice(actions)
        else:
            q_values = [self.get_q_value(state, action) for action in actions]
            action = actions[np.argmax(q_values)]

        return action

    def update_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon -= self.epsilon_decay
