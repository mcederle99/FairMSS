import networkx as nx
import math
import numpy as np


# np.random.seed(0)


# node_list is a vector containing the number of nodes for each category
def generate_network(node_list):
    g = nx.Graph()

    n_categories = len(node_list)
    if n_categories == 2:
        categories = [0, 4]
    elif n_categories == 3:
        categories = [0, 2, 4]
    elif n_categories == 4:
        categories = [0, 1, 3, 4]
    else:
        categories = [0, 1, 2, 3, 4]

    prev = 0
    for i in range(n_categories):
        if i > 0:
            category_i_nodes = range(prev, prev + node_list[i])
            prev += node_list[i]
        else:
            category_i_nodes = range(node_list[i])
            prev = node_list[i]

        for node in category_i_nodes:
            g.add_node(node, station=categories[i], bikes=0)

    return g


def generate_bike_distribution(g, total_bikes, n_cat, distribution_type='wg'):

    # distribution_type = 'wg' or 'u'
    # if 'wg':
    # weighted gaussian initial distribution according to a prior for each category
    # if 'u':
    # uniform distribution among all the stations

    for _, node_data in g.nodes(data=True):
        node_data['bikes'] = 0

    if n_cat == 2:
        categories = [0, 4]
    elif n_cat == 3:
        categories = [0, 2, 4]
    elif n_cat == 4:
        categories = [0, 1, 3, 4]
    else:
        categories = [0, 1, 2, 3, 4]

    nodes = list(g.nodes)
    nodes_per_category = []
    for i in categories:
        nodes_per_category.append([node for node in nodes if g.nodes[node]['station'] == i])

    if n_cat == 2:
        mu_0 = 200 / 60
        mu_4 = 500 / 10
        mu = [mu_0, mu_4]
        upper_bounds = [15, 60]
    elif n_cat == 3:
        mu_0 = total_bikes * 0.2 / 60
        mu_2 = total_bikes * 0.3 / 30
        mu_4 = total_bikes * 0.5 / 10
        mu = [mu_0, mu_2, mu_4]
        upper_bounds = [15, 25, 60]
    elif n_cat == 4:
        mu_0 = 200 / 60
        mu_1 = 300 / 45
        mu_3 = 400 / 20
        mu_4 = 500 / 10
        mu = [mu_0, mu_1, mu_3, mu_4]
        upper_bounds = [15, 20, 40, 60]
    else:
        mu_0 = 200 / 60
        mu_1 = 300 / 45
        mu_2 = 300 / 30
        mu_3 = 400 / 20
        mu_4 = 500 / 10
        mu = [mu_0, mu_1, mu_2, mu_3, mu_4]
        upper_bounds = [15, 20, 25, 40, 60]

    if distribution_type == 'wg':
        for i in range(n_cat):
            for node in nodes_per_category[i]:
                g.nodes[node]['bikes'] = math.ceil(np.random.normal(mu[i], 1))
                if g.nodes[node]['bikes'] < 0:
                    g.nodes[node]['bikes'] = 0
                if g.nodes[node]['bikes'] > upper_bounds[i]:
                    g.nodes[node]['bikes'] = upper_bounds[i]

    elif distribution_type == 'u':
        bikes_per_node = total_bikes // len(nodes)
        remainder_bikes = total_bikes % len(nodes)

        for node in nodes:
            g.nodes[node]['bikes'] = bikes_per_node

        for i in range(remainder_bikes):
            g.nodes[nodes[i]]['bikes'] += 1

        for i in range(n_cat):
            for node in nodes_per_category[i]:
                if g.nodes[node]['bikes'] > upper_bounds[i]:
                    g.nodes[node]['bikes'] = upper_bounds[i]
