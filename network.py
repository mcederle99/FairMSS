import networkx as nx


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
