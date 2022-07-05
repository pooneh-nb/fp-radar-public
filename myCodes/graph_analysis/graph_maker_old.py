import networkx as nx
import multiprocessing
from myCodes.AST import utilities
import json
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
import dill
from networkx.readwrite import json_graph


def create_nodes():
    nodes = []

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", "rt") as op:
        api_hash_weight = json.load(op)
    for key_api, value in api_hash_weight.items():
        nodes.append((key_api, {'node_weight': value['node_weight']}))
        #G.add_node(key_api, weight=value['node_weight'])
    #print(list(G.nodes))

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/nodes_tuple.json", "w") as nod:
        json.dump(nodes, nod, indent=4)


def create_edges():
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", "rt") as op:
        api_hash_weight = json.load(op)

    edges = []
    all_api_keys = list(api_hash_weight.keys())
    print(len(all_api_keys))
    for idx, key in enumerate(all_api_keys):
        print(idx)
        check_hashes = set(api_hash_weight[key]['hash'])
        for i in range(idx + 1, len(all_api_keys)):
            current_hashes = set(api_hash_weight[all_api_keys[i]]['hash'])
            intersection_set = check_hashes.intersection(current_hashes)
            if len(intersection_set) > 0:
                edge_weight = len(intersection_set)
                edges.append((key, all_api_keys[i], {'weight': edge_weight}))

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/edges_tuple.json", "w") as ed:
        json.dump(edges, ed, indent=4)


def seprate_weights():
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/wayback_results/2020/nodes_tuple.json", "rt") as nod:
        nodes_list = json.load(nod)
    with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/wayback_results/2020/edges_tuple.json", "rt") as ed:
        edges_list = json.load(ed)

    edge_weight = []
    for ed in range(len(edges_list)):
        edge_weight.append(edges_list[ed][2]['edge_weight'])
    print(edge_weight)
    print(edges_list)


def normalization():
    node_list = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/nodes_tuple.json")
    edge_list = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/edges_tuple.json")

    node_weight = set()
    for nd in node_list:
        if nd[1]['node_weight'] != 10000:
            node_weight.add(nd[1]['node_weight'])

    edge_weight = set()
    for wt in edge_list:
        edge_weight.add(wt[2]['weight'])

    node_max = max(node_weight) + 5
    edge_max = max(edge_weight)

    idx = 0
    for nd in node_list:
        if nd[1]['node_weight'] != 10000:
            a = node_list[idx][1]['node_weight']
            node_list[idx][1]['node_weight'] = round(node_list[idx][1]['node_weight']/ node_max, 5)
            a = node_list[idx][1]['node_weight']
            idx += 1
        else:
            a = node_list[idx][1]['node_weight']
            node_list[idx][1]['node_weight'] = 1
            a = node_list[idx][1]['node_weight']
            idx +=1

    edge_weight = set()
    idxw = 0
    for wt in edge_list:
        b = edge_list[idxw][2]['weight']
        edge_list[idxw][2]['weight'] = round(edge_list[idxw][2]['weight'] / edge_max, 5)
        b = edge_list[idxw][2]['weight']
        idxw += 1

    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/normalized_nodes_tuple.json", node_list)
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/normalized_edges_tuple.json", edge_list)

def graph():
    # upload nodes
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/normalized_nodes_tuple.json", "rt") as nod:
        nodes_list = json.load(nod)
    nodes = [tuple(l) for l in nodes_list]
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/normalized_edges_tuple.json", "rt") as ed:
        edges_list = json.load(ed)
    edges = [tuple(ee) for ee in edges_list]
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    #pos = nx.nx_agraph.graphviz_layout(G)

    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_pos.json", 'w') as a:
        #json.dump(pos, a, indent=4)
    #with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_pos.json", 'w') as a:
        #pos = json.load(a)

    #nx.draw(G, pos=pos)
    #write_dot(G, 'file.dot')
    #nx.draw(G, with_labels=True)
    #plt.show()

    #api_graph_json = json_graph.node_link_data(api_graph)
    #utilities.write_json(json_graph_addr, api_graph_json)

    data = json_graph.node_link_data(G)
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/Graph_2019.json", data)

def define_node_degrees():
    #Define an empty key-value for degree

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", 'r') as ap:
        api_prop = json.load(ap)

    for api_key, value in api_prop.items():
        api_prop[api_key]['node_degree'] = 0

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", 'w') as a:
        json.dump(api_prop, a, indent=4)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", 'r') as ap:
        api_prop = json.load(ap)
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/normalized_edges_tuple.json", 'r') as ed:
        edge_list = json.load(ed)

    for edge in edge_list:
        api_prop[edge[0]]['node_degree'] = api_prop[edge[0]]['node_degree'] + 1
        api_prop[edge[1]]['node_degree'] = api_prop[edge[1]]['node_degree'] + 1

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/api_hash_frac.json", 'w') as a:
        json.dump(api_prop, a, indent=4)


def graph_pruning():
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/edges_tuple.json", 'rt') as edge:
        edge_list = json.load(edge)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/api_hash_frac_louvian_0.94.json", 'r') as ap:
        api_prop = json.load(ap)

    pruned_edge_list = []
    pruned_nodes_list = []
    pruned_nodes_set = set()

    for edge in edge_list:
        if edge[2]['edge_weight'] > 10:
            if api_prop[edge[0]]['node_weight'] > 0.2 and api_prop[edge[1]]['node_weight'] > 0.2:
                pruned_edge_list.append((edge[0], edge[1], {'weight': edge[2]['edge_weight']}))
        else:
            api_prop[edge[0]]['node_degree'] = api_prop[edge[0]]['node_degree'] - 1
            api_prop[edge[1]]['node_degree'] = api_prop[edge[1]]['node_degree'] - 1

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_edge.json", 'w') as a:
        json.dump(pruned_edge_list, a, indent=4)

    pruned_edge = list(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_edge.json"))
    for edge in pruned_edge:
        pruned_nodes_set.add(edge[0])
        pruned_nodes_set.add(edge[1])

    for api_key, value in api_prop.items():
        if value['node_weight'] > 2:
            pruned_nodes_set.add(api_key)

    for nod in pruned_nodes_set:
        pruned_nodes_list.append([nod, {'node_weight': api_prop[nod]['node_weight']}])

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_api_hash_frac_louvian_0.94.json", 'w') as a:
        json.dump(api_prop, a, indent=4)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_node.json", 'w') as a:
        json.dump(pruned_nodes_list, a, indent=4)

    pruned_node = dict(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_node.json"))
    pruned_api_general = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_api_hash_frac_louvian_0.94.json")
    for key in pruned_api_general.copy():
        if key not in list(pruned_node):
            del pruned_api_general[key]
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_api_hash_frac_louvian_0.94.json",
                         pruned_api_general)


# in this function we add the position of api_keywords
# pos = nx.spring_layout(G, weight='weight')
# utilities.write_dill("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_pos.json", pos)
def add_position():
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/api_hash_frac.json", 'rt') as node:
        nodes = json.load(node)
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pos.json", 'rb') as data:
        position = dill.load(data)

    for api_key, pos in position.items():
        nodes[api_key]['x_pos'] = pos.item(0)
        nodes[api_key]['y_pos'] = pos.item(1)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/api_hash_frac.json", 'w') as pos:
        json.dump(nodes, pos, indent=4)

def number_of_prouned():
    # node structure after pruning:
    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_edge.json", 'r') as a:
        pruned_edge = json.load(a)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/pruned/pruned_node.json", 'r') as n:
        pruned_node = json.load(n)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/edges_tuple.json", 'rt') as edge:
        edge_list = json.load(edge)

    with open("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/nodes_tuple.json", 'r') as ap:
        node_list = json.load(ap)

    print("origin node numbers", len(node_list))  # 4.387
    print("origin edge numbers", len(edge_list))  # 5.555.863
    print("pruned node numbers", len(pruned_node)) # 3.515
    print("origin edge numbers", len(pruned_edge)) # 3.201.341


def main():
    create_nodes()
    create_edges()
    normalization()
    define_node_degrees()
    graph()


if __name__ == '__main__':
    main()



