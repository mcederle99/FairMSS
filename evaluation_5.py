from environment_5 import FairEnv
from agent import RebalancingAgent
from network import generate_network
from demand import generate_global_demand
import numpy as np
import random
import pickle
import inequalipy as ineq

gini_values_tot = [[], [], [], [], [], [], [], [], [], [], []]
costs_tot = [[], [], [], [], [], [], [], [], [], [], []]
costs_rebalancing = [[], [], [], [], [], [], [], [], [], [], []]
costs_failures = [[], [], [], [], [], [], [], [], [], [], []]
costs_bikes = [[], [], [], [], [], [], [], [], [], [], []]
initial_bikes = [[], [], [], [], [], [], [], [], [], [], []]

# increment_bikes = [[], [], [], [], [], [], [], [], [], [], []]

for beta in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    index = int(beta * 10)
    for seed in range(100, 110):
        np.random.seed(seed)
        random.seed(seed)

        n_bikes = np.load(f'results/bikes_5_cat_{beta}_{seed}.npy')

        gamma = 20

        num_central = 10
        num_subcentral = 20
        num_per = 30
        num_subremote = 40
        num_remote = 60
        num_days = 101

        time_slots = \
            [(0, 12), (12, 24)]
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

        G = generate_network([num_remote, num_subremote, num_per, num_subcentral, num_central])
        all_days_demand_vectors, transformed_demand_vectors = generate_global_demand(
            [num_remote, num_subremote, num_per, num_subcentral, num_central], num_days, demand_params, time_slots)

        agent_0 = RebalancingAgent(0)
        agent_1 = RebalancingAgent(1)
        agent_2 = RebalancingAgent(2)
        agent_3 = RebalancingAgent(3)
        agent_4 = RebalancingAgent(4)

        with open(f"q_tables/q_table_{beta}_5_{seed}_cat0.pkl", "rb") as file:
            agent_0.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_5_{seed}_cat1.pkl", "rb") as file:
            agent_1.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_5_{seed}_cat2.pkl", "rb") as file:
            agent_2.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_5_{seed}_cat3.pkl", "rb") as file:
            agent_3.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_5_{seed}_cat4.pkl", "rb") as file:
            agent_4.q_table = pickle.load(file)

        num_stations = np.sum([num_remote, num_subremote, num_per, num_subcentral, num_central])

        daily_central_failures = []
        daily_subcentral_failures = []
        daily_per_failures = []
        daily_subrem_failures = []
        daily_rem_failures = []
        daily_global_failures = []

        daily_central_rebalancing = []
        daily_subcentral_rebalancing = []
        daily_per_rebalancing = []
        daily_subrem_rebalancing = []
        daily_rem_rebalancing = []
        daily_global_rebalancing = []

        daily_global_costs = []

        agent_0.set_epsilon(0.0)
        agent_1.set_epsilon(0.0)
        agent_2.set_epsilon(0.0)
        agent_3.set_epsilon(0.0)
        agent_4.set_epsilon(0.0)

        eval_env = FairEnv(G, transformed_demand_vectors, beta, gamma)
        state = eval_env.reset()

        for day in range(101):
            ret = 0

            central_fails = 0
            subcentral_fails = 0
            per_fails = 0
            subrem_fails = 0
            rem_fails = 0
            global_fails = 0

            central_rebalancing = 0
            subcentral_rebalancing = 0
            per_rebalancing = 0
            subrem_rebalancing = 0
            rem_rebalancing = 0
            global_rebalancing = 0

            costs = 0

            for time in (0, 1):
                actions = np.zeros(num_stations, dtype=np.int64)
                if day > 0:
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

                next_state, reward, failures = eval_env.step(actions)

                ret += np.sum(reward)

                central_fails += np.sum(failures[150:])
                subcentral_fails += np.sum(failures[130:150])
                per_fails += np.sum(failures[100:130])
                subrem_fails += np.sum(failures[60:100])
                rem_fails += np.sum(failures[:60])
                global_fails += np.sum(failures)

                for a in range(len(actions)):
                    if actions[a] != 0:
                        global_rebalancing += 1
                        if a < 60:
                            rem_rebalancing += 1
                            costs += 1
                        elif a < 100:
                            subrem_rebalancing += 1
                            costs += 0.8
                        elif a < 130:
                            per_rebalancing += 1
                            costs += 0.4
                        elif a < 150:
                            subcentral_rebalancing += 1
                            costs += 0.3
                        else:
                            central_rebalancing += 1
                            costs += 0.1

                state = next_state

            if day > 0:
                daily_central_failures.append(central_fails / 10)
                daily_subcentral_failures.append(subcentral_fails / 20)
                daily_per_failures.append(per_fails / 30)
                daily_subrem_failures.append(subrem_fails / 40)
                daily_rem_failures.append(rem_fails / 60)
                daily_global_failures.append(global_fails)

                daily_central_rebalancing.append(central_rebalancing / 10)
                daily_subcentral_rebalancing.append(subcentral_rebalancing / 20)
                daily_per_rebalancing.append(per_rebalancing / 30)
                daily_subrem_rebalancing.append(subrem_rebalancing / 40)
                daily_rem_rebalancing.append(rem_rebalancing / 60)
                daily_global_rebalancing.append(global_rebalancing)

                daily_global_costs.append(costs)

            if day == 0:
                bici_s = 0
                for i in range(num_stations):
                    bici_s += G.nodes[i]['bikes']
                initial_bikes[index].append(bici_s)

        # bici_f = 0
        # for i in range(num_stations):
        #     bici_f += G.nodes[i]['bikes']
        # increment_bikes[index].append((bici_f - bici_s)/bici_s*100)

        central_requests = 0
        subcentral_requests = 0
        per_requests = 0
        subrem_requests = 0
        rem_requests = 0
        global_requests = 0

        for day in range(101):
            for i in range(24):
                for j in range(num_stations):
                    if j < 60:
                        if all_days_demand_vectors[day][j][i] < 0:
                            rem_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    elif j < 100:
                        if all_days_demand_vectors[day][j][i] < 0:
                            subrem_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    elif j < 130:
                        if all_days_demand_vectors[day][j][i] < 0:
                            per_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    elif j < 150:
                        if all_days_demand_vectors[day][j][i] < 0:
                            subcentral_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    else:
                        if all_days_demand_vectors[day][j][i] < 0:
                            central_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])

        central_requests = central_requests / 101 / 10
        subcentral_requests = subcentral_requests / 101 / 20
        per_requests = per_requests / 101 / 30
        subrem_requests = subrem_requests / 101 / 40
        rem_requests = rem_requests / 101 / 60
        global_requests = global_requests / 100

        failure_rate_central = np.mean(daily_central_failures) / central_requests * 100
        failure_rate_subcentral = np.mean(daily_subcentral_failures) / subcentral_requests * 100
        failure_rate_per = np.mean(daily_per_failures) / per_requests * 100
        failure_rate_subrem = np.mean(daily_subrem_failures) / subrem_requests * 100
        failure_rate_rem = np.mean(daily_rem_failures) / rem_requests * 100
        failure_rate_global = np.mean(daily_global_failures) / global_requests * 100

        gini_coefficient = np.round(ineq.gini([failure_rate_central, failure_rate_subcentral, failure_rate_per,
                                               failure_rate_subrem, failure_rate_rem]), 3)
        gini_values_tot[index].append(gini_coefficient)
        costs_tot[index].append(np.mean(daily_global_costs) + n_bikes / 100 + failure_rate_global / 10)
        costs_rebalancing[index].append(np.mean(daily_global_costs))
        costs_failures[index].append(failure_rate_global)
        costs_bikes[index].append(n_bikes)

np.save('results/gini_5_cat_10seeds.npy', gini_values_tot)
np.save('results/cost_5_cat_10seeds.npy', costs_tot)
np.save('results/cost_reb_5_cat_10seeds.npy', costs_rebalancing)
np.save('results/cost_fail_5_cat_10seeds.npy', costs_failures)
np.save('results/cost_bikes_5_cat_10seeds.npy', costs_bikes)
# np.save('results/increment_bikes_5_cat_10seeds.npy', increment_bikes)
np.save('results/initial_bikes_5_cat_10seeds.npy', initial_bikes)
