from environment import FairEnv
from agent import RebalancingAgent
from network import generate_network, generate_bike_distribution
from demand import generate_global_demand
import numpy as np
import random
import pickle
import inequalipy as ineq

n_bikes_0 = [1502, 1524, 1668, 1727, 1762, 1717, 1779, 1804, 1730, 1913, 1940]
n_bikes_1 = [1602, 1710, 1663, 1577, 1807, 1675, 1724, 1777, 1794, 1840, 1889]
n_bikes_2 = [1503, 1491, 1698, 1732, 1672, 1767, 1693, 1817, 1783, 1822, 1755]
n_bikes_3 = [1618, 1539, 1673, 1564, 1611, 1721, 1762, 1867, 1752, 1832, 1804]
n_bikes_4 = [1567, 1671, 1611, 1713, 1701, 1670, 1766, 1762, 1787, 1780, 1855]
n_bikes_5 = [1605, 1556, 1568, 1690, 1653, 1740, 1809, 1794, 1708, 1873, 1830]
n_bikes_6 = [1566, 1588, 1751, 1644, 1770, 1756, 1756, 1747, 1900, 1801, 1892]
n_bikes_7 = [1561, 1552, 1659, 1619, 1693, 1834, 1772, 1801, 1877, 1853, 1775]
n_bikes_8 = [1609, 1597, 1616, 1706, 1695, 1670, 1884, 1741, 1781, 1802, 1884]
n_bikes_9 = [1477, 1708, 1546, 1664, 1681, 1804, 1775, 1840, 1720, 1768, 1837]
n_bikes = [n_bikes_0, n_bikes_1, n_bikes_2, n_bikes_3, n_bikes_4, n_bikes_5,
           n_bikes_6, n_bikes_7, n_bikes_8, n_bikes_9]

gini_values_tot = [[], [], [], [], [], [], [], [], [], [], []]
costs_tot = [[], [], [], [], [], [], [], [], [], [], []]
bikes_tot = [[], [], [], [], [], [], [], [], [], [], []]
max_possible_bikes = [[], [], [], [], [], [], [], [], [], [], []]
for beta in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    index = int(beta * 10)
    for seed in range(10):
        np.random.seed(seed)
        random.seed(seed)

        gamma = 20

        num_central = 10
        num_peripheral = 30
        num_remote = 60
        num_days = 101
        # time_slots =\
        #     [(0, 4), (4, 7), (7, 10), (10, 11), (11, 13), (13, 14), (14, 17), (17, 20), (20, 24)]
        # central_params =\
        #     [(3.9, 1.6), (4.4, 2), (13, 1), (11.9, 2), (2, 2), (5, 5), (4, 10), (6.8, 10), (2, 2)]
        # peripheral_params =\
        #     [(2, 1), (1, 1), (3, 3), (2, 1.5), (1, 1), (2, 1), (3, 2), (2, 1), (1, 1)]
        # remote_params =\
        #     [(0.1, 1), (0.1, 1), (0.1, 2.1), (0.1, 2), (1, 1), (2, 2), (1, 1), (1, 1), (1, 1)]

        # central_params = [(1, 1), (1, 1), (0.5, 2), (0.5, 2), (1, 1), (1, 1.5), (2, 1), (2, 1), (1, 1)]
        # peripheral_params = [(2, 2), (2, 2), (2, 1.5), (1.5, 1), (2, 2), (1, 2), (3, 4), (2, 3), (2, 2)]
        # remote_params = [(2, 2), (2, 2), (16.5, 9), (15, 7.5), (2, 2), (8, 2), (4, 10), (1, 4), (2, 2)]

        time_slots = \
            [(0, 12), (12, 24)]
        remote_params = \
            [(0.3, 2), (1.5, 0.3)]
        peripheral_params = \
            [(3.3, 1.5), (1.5, 3.3)]
        central_params = \
            [(13.8, 9), (12, 13.8)]

        G = generate_network([num_remote, num_peripheral, num_central])
        all_days_demand_vectors, transformed_demand_vectors = (
            generate_global_demand([num_remote, num_peripheral, num_central], num_days,
                                   [remote_params, peripheral_params, central_params], time_slots))

        # DEBUG DEMAND
        # central_requests = 0
        # per_requests = 0
        # rem_requests = 0
        # global_requests = 0
        #
        # central_arrivals = 0
        # per_arrivals = 0
        # rem_arrivals = 0
        # global_arrivals = 0
        #
        # for day in range(100):
        #     for i in range(12, 24):
        #         for j in range(100):
        #             if j < 60:
        #                 if all_days_demand_vectors[day][j][i] < 0:
        #                     rem_requests += abs(all_days_demand_vectors[day][j][i])
        #                     global_requests += abs(all_days_demand_vectors[day][j][i])
        #                 else:
        #                     rem_arrivals += abs(all_days_demand_vectors[day][j][i])
        #                     global_arrivals += abs(all_days_demand_vectors[day][j][i])
        #             elif j < 90:
        #                 if all_days_demand_vectors[day][j][i] < 0:
        #                     per_requests += abs(all_days_demand_vectors[day][j][i])
        #                     global_requests += abs(all_days_demand_vectors[day][j][i])
        #                 else:
        #                     per_arrivals += abs(all_days_demand_vectors[day][j][i])
        #                     global_arrivals += abs(all_days_demand_vectors[day][j][i])
        #             else:
        #                 if all_days_demand_vectors[day][j][i] < 0:
        #                     central_requests += abs(all_days_demand_vectors[day][j][i])
        #                     global_requests += abs(all_days_demand_vectors[day][j][i])
        #                 else:
        #                     central_arrivals += abs(all_days_demand_vectors[day][j][i])
        #                     global_arrivals += abs(all_days_demand_vectors[day][j][i])
        #
        # central_requests = central_requests / 100 / 10
        # per_requests = per_requests / 100 / 30
        # rem_requests = rem_requests / 100 / 60
        # global_requests = global_requests / 100
        #
        # central_arrivals = central_arrivals / 100 / 10
        # per_arrivals = per_arrivals / 100 / 30
        # rem_arrivals = rem_arrivals / 100 / 60
        # global_arrivals = global_arrivals / 100
        #
        # print(f'Average daily requests in a central station: {central_requests}')
        # print(f'Average daily requests in a peripheral station: {per_requests}')
        # print(f'Average daily requests in a remote station: {rem_requests}')
        # print(f'Average daily requests in the network: {global_requests}')
        # print("==================================")
        # print(f'Average daily arrivals in a central station: {central_arrivals}')
        # print(f'Average daily arrivals in a peripheral station: {per_arrivals}')
        # print(f'Average daily arrivals in a remote station: {rem_arrivals}')
        # print(f'Average daily arrivals in the network: {global_arrivals}')
        # # END DEBUG DEMAND
        # raise KeyboardInterrupt

        agent_0 = RebalancingAgent(0)
        agent_2 = RebalancingAgent(2)
        agent_4 = RebalancingAgent(4)

        with open(f"q_tables/q_table_{beta}_3_{seed}_cat0.pkl", "rb") as file:
            agent_0.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_3_{seed}_cat2.pkl", "rb") as file:
            agent_2.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_3_{seed}_cat4.pkl", "rb") as file:
            agent_4.q_table = pickle.load(file)

        # agent_4.print_q_table()
        # raise KeyboardInterrupt

        num_stations = 100
        # generate_bike_distribution(G, 1000, 3, 'wg')

        daily_central_failures = []
        daily_per_failures = []
        daily_rem_failures = []
        daily_global_failures = []

        daily_central_rebalancing = []
        daily_per_rebalancing = []
        daily_rem_rebalancing = []
        daily_global_rebalancing = []

        daily_global_costs = []

        agent_0.set_epsilon(0.0)
        agent_2.set_epsilon(0.0)
        agent_4.set_epsilon(0.0)

        eval_env = FairEnv(G, transformed_demand_vectors, beta, gamma)
        state = eval_env.reset()
        # initial_bikes = 0
        # initial_rem_bikes = 0
        # initial_per_bikes = 0
        # initial_central_bikes = 0
        # for i in range(100):
        #     initial_bikes += G.nodes[i]['bikes']
        #     if i < 60:
        #         initial_rem_bikes += G.nodes[i]['bikes']
        #     elif i < 90:
        #         initial_per_bikes += G.nodes[i]['bikes']
        #     else:
        #         initial_central_bikes += G.nodes[i]['bikes']
        # daily_bikes = 0
        # daily_central_bikes = 0
        # daily_per_bikes = 0
        # daily_rem_bikes = 0

        for day in range(101):
            # for i in range(100):
            #     daily_bikes += G.nodes[i]['bikes']
            #     if i < 60:
            #         daily_rem_bikes += G.nodes[i]['bikes']
            #     elif i < 90:
            #         daily_per_bikes += G.nodes[i]['bikes']
            #     else:
            #         daily_central_bikes += G.nodes[i]['bikes']
            ret = 0

            central_fails = 0
            per_fails = 0
            rem_fails = 0
            global_fails = 0

            central_rebalancing = 0
            per_rebalancing = 0
            rem_rebalancing = 0
            global_rebalancing = 0

            costs = 0

            for time in (0, 1):
                actions = np.zeros(num_stations, dtype=np.int64)
                if day > 0:
                    for i in range(num_stations):
                        if G.nodes[i]['station'] == 0:
                            actions[i] = agent_0.decide_action(state[i])
                        elif G.nodes[i]['station'] == 2:
                            actions[i] = agent_2.decide_action(state[i])
                        else:
                            actions[i] = agent_4.decide_action(state[i])

                next_state, reward, failures = eval_env.step(actions)

                ret += np.sum(reward)

                central_fails += np.sum(failures[90:])
                per_fails += np.sum(failures[60:90])
                rem_fails += np.sum(failures[:60])
                global_fails += np.sum(failures)

                for a in range(len(actions)):
                    if actions[a] != 0:
                        global_rebalancing += 1
                        if a < 60:
                            rem_rebalancing += 1
                            costs += 1
                        elif a < 90:
                            per_rebalancing += 1
                            costs += 0.4
                        else:
                            central_rebalancing += 1
                            costs += 0.1

                state = next_state

            if day > 0:
                daily_central_failures.append(central_fails/10)
                daily_per_failures.append(per_fails/30)
                daily_rem_failures.append(rem_fails/60)
                daily_global_failures.append(global_fails)

                daily_central_rebalancing.append(central_rebalancing/10)
                daily_per_rebalancing.append(per_rebalancing/30)
                daily_rem_rebalancing.append(rem_rebalancing/60)
                daily_global_rebalancing.append(global_rebalancing)

                daily_global_costs.append(costs)

        central_requests = 0
        per_requests = 0
        rem_requests = 0
        global_requests = 0

        for day in range(101):
            for i in range(24):
                for j in range(100):
                    if j < 60:
                        if all_days_demand_vectors[day][j][i] < 0:
                            rem_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    elif j < 90:
                        if all_days_demand_vectors[day][j][i] < 0:
                            per_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    else:
                        if all_days_demand_vectors[day][j][i] < 0:
                            central_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])

        central_requests = central_requests / 101 / 10
        per_requests = per_requests / 101 / 30
        rem_requests = rem_requests / 101 / 60
        global_requests = global_requests / 101

        failure_rate_central = np.mean(daily_central_failures) / central_requests * 100
        failure_rate_per = np.mean(daily_per_failures) / per_requests * 100
        failure_rate_rem = np.mean(daily_rem_failures) / rem_requests * 100
        failure_rate_global = np.mean(daily_global_failures) / global_requests * 100
        # print(f'Global failure rate: {failure_rate_global}')
        # print(f'Central failure rate: {failure_rate_central}')
        # print(f'Peripheral failure rate: {failure_rate_per}')
        # print(f'Remote failure rate: {failure_rate_rem}')

        # daily_bikes = daily_bikes / 100
        # daily_central_bikes = daily_central_bikes / 100
        # daily_per_bikes = daily_per_bikes / 100
        # daily_rem_bikes = daily_rem_bikes / 100
        # bike_increment = (daily_bikes - initial_bikes) / initial_bikes * 100
        # bike_increment_central = (daily_central_bikes - initial_central_bikes) / initial_central_bikes * 100
        # bike_increment_per = (daily_per_bikes - initial_per_bikes) / initial_per_bikes * 100
        # bike_increment_rem = (daily_rem_bikes - initial_rem_bikes) / initial_rem_bikes * 100
        # max_bike_increment = (2250 - initial_bikes) / initial_bikes * 100
        # max_bike_increment_central = (600 - initial_central_bikes) / initial_central_bikes * 100
        # max_bike_increment_per = (750 - initial_per_bikes) / initial_per_bikes * 100
        # max_bike_increment_rem = (900 - initial_rem_bikes) / initial_rem_bikes * 100

        # print(f"Global increment: {bike_increment}, max allowed: {max_bike_increment}")
        # print(f"Central increment: {bike_increment_central}, max allowed: {max_bike_increment_central}")
        # print(f"Per increment: {bike_increment_per}, max allowed: {max_bike_increment_per}")
        # print(f"Rem increment: {bike_increment_rem}, max allowed: {max_bike_increment_rem}")
        # print("------------------------")

        gini_coefficient = np.round(ineq.gini([failure_rate_central, failure_rate_per, failure_rate_rem]), 3)
        # print(f"Gini coefficient: {gini_coefficient}")
        gini_values_tot[index].append(gini_coefficient)
        costs_tot[index].append(np.mean(daily_global_costs) + n_bikes[seed][index] / 100 + failure_rate_global / 10)
        # bikes_tot[index].append(bike_increment)
        # max_possible_bikes[index].append(max_bike_increment)

np.save('results/gini_3_cat_fixed_alsodemand_10seeds.npy', gini_values_tot)
np.save('results/cost_3_cat_fixed_alsodemand_10seeds.npy', costs_tot)
# np.save('results/bikes_3_cat_fixed_alsodemand.npy', bikes_tot)
# np.save('results/max_bikes_3_cat_fixed_alsodemand.npy', max_possible_bikes)
