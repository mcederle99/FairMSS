import numpy as np


np.random.seed(0)


class FairEnv:

    def __init__(self, graph, demand_vectors, temperature):
        self.G = graph
        self.demand_vectors = demand_vectors
        self.num_stations = len(list(self.G.nodes))
        self.hour = 0
        self.day = 0
        self.next_rebalancing_hour = 11
        self.temperature = temperature

    def action_space(self):
        actions = [-30, -20, -10, 0, 5, 10, 20]

        return np.random.choice(actions)

    def observation_space(self):
        state = []

        n_bikes = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        state.append(np.random.choice(n_bikes))

        station_type = [0, 1, 2]  # equivalent to ['central', 'peripheral', 'remote']
        state.append(np.random.choice(station_type))

        time = [0, 1]  # equivalent to ['morning', 'evening']
        state.append(np.random.choice(time))

        return state

    def get_state(self):
        state = np.zeros((self.num_stations, 3), dtype=np.int64)
        failures = [0] * self.num_stations

        time = 0 if self.next_rebalancing_hour == 11 else 1
        while self.hour <= self.next_rebalancing_hour:
            for i in range(self.num_stations):
                n_bikes = self.G.nodes[i]['bikes']

                demand_list = self.demand_vectors[self.day][i][self.hour]
                for demand_change in demand_list:
                    n_bikes += demand_change
                    if n_bikes < 0:
                        n_bikes = 0
                        failures[i] += 1

                self.G.nodes[i]['bikes'] = n_bikes

                state[i] = [n_bikes, self.G.nodes[i]['station'], time]

            self.hour += 1

        self.next_rebalancing_hour = 23 if self.hour == 12 else 11
        if self.next_rebalancing_hour == 11:
            self.day += 1
            self.hour = 0
            if self.day == 1000:
                self.day = 0

        return state, failures

    def compute_reward(self, action, failures):  # reward is a (num_stations, 1) vector
        rewards = np.zeros(self.num_stations)

        for i in range(self.num_stations):
            if self.G.nodes[i]['station'] == 0:
                beta = -self.temperature
            elif self.G.nodes[i]['station'] == 2:
                beta = self.temperature
            else:
                beta = 0

            rewards[i] = - (1 + beta) * failures[i] - 0.5 * action[i]

        return rewards

    def reset(self):
        self.hour = 0
        self.day = 0
        self.next_rebalancing_hour = 11

        state = np.zeros((self.num_stations, 3), dtype=np.int64)
        for i in range(self.num_stations):
            state[i] = [self.G.nodes[i]['bikes'], self.G.nodes[i]['station'], 0]

        return state

    def step(self, action):  # action is a (num_stations, 1) vector
        for i in range(self.num_stations):
            self.G.nodes[i]['bikes'] += action[i]

        state, failures = self.get_state()

        reward = self.compute_reward(action, failures)

        return state, reward, failures
