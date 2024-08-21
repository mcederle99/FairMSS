import networkx as nx

num_central = 10
num_peripheral = 30
num_desolate = 60

G = nx.Graph()

central_nodes = range(num_central)
peripheral_nodes = range(num_central, num_central + num_peripheral)
desolate_nodes = range(num_central + num_peripheral, num_central +
                       num_peripheral + num_desolate)

for node in central_nodes:
    G.add_node(node, station=0, bikes=0)

for node in peripheral_nodes:
    G.add_node(node, station=1, bikes=0)

for node in desolate_nodes:
    G.add_node(node, station=2, bikes=0)