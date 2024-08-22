import networkx as nx
import math
import numpy as np


np.random.seed(0)


def generate_network(num_central, num_peripheral, num_remote):
    g = nx.Graph()

    central_nodes = range(num_central)
    peripheral_nodes = range(num_central, num_central + num_peripheral)
    remote_nodes = range(num_central + num_peripheral, num_central + num_peripheral + num_remote)

    for node in central_nodes:
        g.add_node(node, station=0, bikes=0)

    for node in peripheral_nodes:
        g.add_node(node, station=1, bikes=0)

    for node in remote_nodes:
        g.add_node(node, station=2, bikes=0)

    return g


def generate_bike_distribution(g, total_bikes, distribution_type='wg'):

    # distribution_type = 'wg' or 'u'
    # if 'wg':
    # half of the bikes go to the central stations
    # the 75% of the remaining bikes go to the peripheral stations
    # the rest goes to the remote stations

    for _, node_data in g.nodes(data=True):
        node_data['bikes'] = 0

    nodes = list(g.nodes)
    central_nodes = [node for node in nodes if g.nodes[node]['station'] == 0]
    peripheral_nodes = [node for node in nodes if g.nodes[node]['station'] == 1]
    remote_nodes = [node for node in nodes if g.nodes[node]['station'] == 2]

    if distribution_type == 'wg':
        mu_central = total_bikes / 2 / len(central_nodes)
        mu_peripheral = total_bikes / 2 * 0.7 / len(peripheral_nodes)
        mu_remote = total_bikes / 2 * 0.3 / len(remote_nodes)

        for node in central_nodes:
            g.nodes[node]['bikes'] = math.ceil(np.random.normal(mu_central, 1))
            if g.nodes[node]['bikes'] < 0:
                g.nodes[node]['bikes'] = 0
        for node in peripheral_nodes:
            g.nodes[node]['bikes'] = math.ceil(np.random.normal(mu_peripheral, 1))
            if g.nodes[node]['bikes'] < 0:
                g.nodes[node]['bikes'] = 0
        for node in remote_nodes:
            g.nodes[node]['bikes'] = math.ceil(np.random.normal(mu_remote, 1))
            if g.nodes[node]['bikes'] < 0:
                g.nodes[node]['bikes'] = 0

    elif distribution_type == 'u':
        bikes_per_node = total_bikes // len(nodes)
        remainder_bikes = total_bikes % len(nodes)

        for node in nodes:
            g.nodes[node]['bikes'] = bikes_per_node

        for i in range(remainder_bikes):
            g.nodes[nodes[i]]['bikes'] += 1
          