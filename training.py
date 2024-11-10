from agent import RebalancingAgent
from network import generate_network
from demand import generate_global_demand
import numpy as np
import random
import pickle
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--beta", default=0, type=float)
parser.add_argument("--categories", default=0, type=int)
parser.add_argument("--seed", default=0, type=int)
args = parser.parse_args()

beta = args.beta / 10
gamma = 20
file_path = f'training_times_{args.categories}.txt'

num_days = 1000
time_slots =\
    [(0, 12), (12, 24)]

if args.categories == 2:
    from environment_2 import FairEnv
    demand_params_0 = \
        [(0.3, 2), (1.5, 0.3)]
    demand_params_4 = \
        [(13.8, 3.6), (6.6, 13.8)]
    demand_params = [demand_params_0, demand_params_4]
    node_list = [60, 10]

elif args.categories == 3:
    from environment_3 import FairEnv
    demand_params_0 = \
        [(0.3, 2), (1.5, 0.3)]
    demand_params_2 = \
        [(3.3, 1.5), (1.5, 3.3)]
    demand_params_4 = \
        [(13.8, 9), (12, 13.8)]
    demand_params = [demand_params_0, demand_params_2, demand_params_4]
    node_list = [60, 30, 10]

elif args.categories == 4:
    from environment_4 import FairEnv
    demand_params_0 = \
        [(0.3, 2), (1.5, 0.3)]
    demand_params_1 = \
        [(0.45, 3), (2.25, 0.45)]
    demand_params_3 = \
        [(9.2, 2.4), (4.4, 9.2)]
    demand_params_4 = \
        [(13.8, 7), (9, 13.8)]
    demand_params = [demand_params_0, demand_params_1, demand_params_3, demand_params_4]
    node_list = [60, 40, 20, 10]

elif args.categories == 5:
    from environment_5 import FairEnv

    demand_params_0 = \
        [(0.3, 2), (1.5, 0.3)]
    demand_params_1 = \
        [(0.45, 3), (2.25, 0.45)]
    demand_params_2 = \
        [(3.3, 1.5), (1.5, 3.3)]
    demand_params_3 = \
        [(9.2, 5.1), (6.6, 9.2)]
    demand_params_4 = \
        [(13.8, 7), (10, 13.8)]
    demand_params = [demand_params_0, demand_params_1, demand_params_2, demand_params_3, demand_params_4]
    node_list = [60, 40, 30, 20, 10]

else:
    raise ValueError("Wrong number of categories. Select among [2, 3, 4, 5]")

agent_0 = RebalancingAgent(0)
agent_1 = RebalancingAgent(1)
agent_2 = RebalancingAgent(2)
agent_3 = RebalancingAgent(3)
agent_4 = RebalancingAgent(4)

G = generate_network(node_list)
all_days_demand_vectors, transformed_demand_vectors = generate_global_demand(node_list, num_days,
                                                                             demand_params, time_slots)

num_stations = np.sum(node_list)
daily_returns = []
daily_failures = []
np.random.seed(args.seed)
random.seed(args.seed)

env = FairEnv(G, transformed_demand_vectors, beta, gamma)
state = env.reset()

start = time.time()
for repeat in range(110):
    for day in range(num_days):
        ret = 0
        fails = 0
        for times in (0, 1):
            actions = np.zeros(num_stations, dtype=np.int64)
            if repeat == 0 and day == 0:
                pass
            else:
                for i in range(num_stations):
                    if G.nodes[i]['station'] == 0:
                        actions[i] = agent_0.decide_action(state[i])
                    elif G.nodes[i]['station'] == 1:
                        actions[i] = agent_1.decide_action(state[i])
                    elif G.nodes[i]['station'] == 2:
                        actions[i] = agent_2.decide_action(state[i])
                    elif G.nodes[i]['station'] == 3:
                        actions[i] = agent_3.decide_action(state[i])
                    else:
                        actions[i] = agent_4.decide_action(state[i])

            next_state, reward, failures = env.step(actions)
            ret += np.sum(reward)

            fails += np.sum(failures)

            if day == 0 and repeat == 0:
                pass
            else:
                for i in range(num_stations):
                    if G.nodes[i]['station'] == 0 and repeat < 19:
                        agent_0.update_q_table(state[i], actions[i], reward[i], next_state[i])
                        agent_0.update_epsilon()
                    elif G.nodes[i]['station'] == 1 and repeat < 28:
                        agent_1.update_q_table(state[i], actions[i], reward[i], next_state[i])
                        agent_1.update_epsilon()
                    elif G.nodes[i]['station'] == 2 and repeat < 37:
                        agent_2.update_q_table(state[i], actions[i], reward[i], next_state[i])
                        agent_2.update_epsilon()
                    elif G.nodes[i]['station'] == 3 and repeat < 55:
                        agent_3.update_q_table(state[i], actions[i], reward[i], next_state[i])
                        agent_3.update_epsilon()
                    elif G.nodes[i]['station'] == 4:
                        agent_4.update_q_table(state[i], actions[i], reward[i], next_state[i])
                        agent_4.update_epsilon()

            state = next_state

        if repeat == 0 and day == 0:
            pass
        else:
            daily_returns.append(ret)
            daily_failures.append(fails)

end = time.time()
with open(file_path, 'a') as file:
    file.write(f'{end - start},\n')

if args.categories == 2:
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat0.pkl", "wb") as file:
        pickle.dump(agent_0.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat4.pkl", "wb") as file:
        pickle.dump(agent_4.q_table, file)
elif args.categories == 3:
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat0.pkl", "wb") as file:
        pickle.dump(agent_0.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat2.pkl", "wb") as file:
        pickle.dump(agent_2.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat4.pkl", "wb") as file:
        pickle.dump(agent_4.q_table, file)
elif args.categories == 4:
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat0.pkl", "wb") as file:
        pickle.dump(agent_0.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat1.pkl", "wb") as file:
        pickle.dump(agent_1.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat3.pkl", "wb") as file:
        pickle.dump(agent_3.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat4.pkl", "wb") as file:
        pickle.dump(agent_4.q_table, file)
else:
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat0.pkl", "wb") as file:
        pickle.dump(agent_0.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat1.pkl", "wb") as file:
        pickle.dump(agent_1.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat2.pkl", "wb") as file:
        pickle.dump(agent_2.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat3.pkl", "wb") as file:
        pickle.dump(agent_3.q_table, file)
    with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}_cat4.pkl", "wb") as file:
        pickle.dump(agent_4.q_table, file)

np.save(f'results/learning_curve_{args.categories}_cat_{args.beta / 10}_{args.seed}.npy', daily_returns)

print(f'Finished simulation with seed: {args.seed}, categories: {args.categories} and beta: {args.beta / 10}')

b = 0
for i in range(num_stations):
    b += G.nodes[i]['bikes']
np.save(f'results/bikes_{args.categories}_cat_{args.beta / 10}_{args.seed}.npy', b)
