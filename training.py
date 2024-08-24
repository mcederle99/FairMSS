from environment import FairEnv
from agent import RebalancingAgent
from network import generate_network, generate_bike_distribution
from demand import generate_global_demand
import numpy as np
import random
import matplotlib.pyplot as plt
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--beta", default=0, type=float)
args = parser.parse_args()

beta = args.beta / 10
gamma = 5

num_central = 10
num_peripheral = 30
num_remote = 60
num_days = 1000
time_slots = [(0, 4), (4, 7), (7, 10), (10, 11), (11, 13), (13, 14), (14, 17), (17, 20), (20, 24)]
central_params = [(2, 2), (2, 2), (13, 1), (7, 1), (2, 2), (1, 6), (1, 10), (1, 7), (2, 2)]
peripheral_params = [(1, 1), (1, 1), (1, 7), (1, 5), (1, 1), (1, 1), (5, 1), (5, 1), (1, 1)]
remote_params = [(1, 1), (1, 1), (1, 2), (1, 2), (1, 1), (1, 2), (2, 1), (2, 1), (1, 1)]

G = generate_network(num_central, num_peripheral, num_remote)
all_days_demand_vectors, transformed_demand_vectors = generate_global_demand(num_central, num_peripheral,
                                                                             num_remote, num_days, central_params,
                                                                             peripheral_params, remote_params,
                                                                             time_slots)

agent = RebalancingAgent()

num_stations = 100
daily_returns = []
daily_failures = []
generate_bike_distribution(G, 1000, 'wg')
np.random.seed(0)
random.seed(0)

env = FairEnv(G, transformed_demand_vectors, beta, gamma)
state = env.reset()

for repeat in range(10):
    for day in range(num_days):
        ret = 0
        fails = 0
        for time in (0, 1):
            actions = np.zeros(num_stations, dtype=np.int64)
            for i in range(num_stations):
                actions[i] = agent.decide_action(state[i])

            next_state, reward, failures = env.step(actions)
            ret += np.sum(reward)
            fails += np.sum(failures)

            for i in range(num_stations):
                agent.update_q_table(state[i], actions[i], reward[i], next_state[i])

            agent.update_epsilon()
            state = next_state

        daily_returns.append(ret)
        daily_failures.append(fails)

plt.plot(daily_returns)
plt.savefig(f"learning_curves/daily_returns_{args.beta / 10}.png")
plt.close()
plt.plot(daily_failures)
plt.savefig(f"learning_curves/daily_failures_{args.beta / 10}.png")
plt.close()

with open(f"q_tables/q_table_{args.beta / 10}.pkl", "wb") as file:
    pickle.dump(agent.q_table, file)

print(f'Finished beta: {args.beta / 10}')
