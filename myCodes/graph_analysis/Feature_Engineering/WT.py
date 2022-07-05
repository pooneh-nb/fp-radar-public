import itertools
from networkx.readwrite import json_graph
import networkx as nx
import math
import numpy as np
from myCodes.AST import utilities
import multiprocessing
from multiprocessing import Pool as ThreadPool
import os
import pandas as pd


# integrate the list of nodes (API keywords) since t-1 to t+1, if you want to predict graph at t+1
def extract_combined_apis(keyword_list_current, api_features_future, completed_keyword_dir):
    # api_features_list1 = utilities.get_files_in_a_directory(api_features_current)
    # api_features_list2 = utilities.get_files_in_a_directory(api_features_future)
    api_features_list = utilities.get_files_in_a_directory(api_features_future)

    keywrd_list = set(keyword_list_current)

    for script in api_features_list:
        script_content = utilities.read_list_compressed(script)
        apis_in_script_content = list(script_content)
        for keyw in apis_in_script_content:
            # print(keyw)
            keywrd_list.add(keyw)
    print(len(keywrd_list))
    utilities.write_json(os.path.join(completed_keyword_dir, "node_list.json"), list(keywrd_list))
    utilities.write_json(os.path.join(completed_keyword_dir, "train/node_list.json"), list(keywrd_list))
    utilities.write_json(os.path.join(completed_keyword_dir, "test/node_list.json"), list(keywrd_list))


# combine and aggregate graphs with its features; year and weight
# sum-up the weights, but keep the first year of creation
def combined_graphs_edges(graph1, graph2, out_dir_test, out_dir_train, year):
    print("Start--> ", year)
    # make a copy of the new graph to ensure that it doesn't change
    new_graph = graph1.copy()

    # iterate over graph2's edges, adding them to graph1
    for node1, node2 in graph2.edges():
        # if that edge already exists, now iterate over the attributes
        if new_graph.has_edge(node1, node2):
            try:
                new_graph.edges[node1, node2]['weight'] += graph2.edges[node1, node2]['weight']
                new_graph.edges[node1, node2]['year'] = graph2.edges[node1, node2]['year']
            except Exception as ex:
                print(ex)

        # otherwise, add the new edge with all its atributes -- first, iterate through those attributes to weight them
        else:
            w = graph2.edges[node1, node2]['weight']
            year_feat = graph2.edges[node1, node2]['year']
            new_graph.add_edge(node1, node2, weight=w, year=year_feat)

    data = json_graph.node_link_data(new_graph)
    utilities.write_json(out_dir_test, data)
    utilities.write_json(out_dir_train, data)

    #data2 = json_graph.node_link_data(new_graph)
    #utilities.write_json(out_dir_train, data2)
    print("End--> ", year)


# calculate some of the WTf each node
def node_wtf_degree_calculation(G, out_dir):
    for node_temp in G.nodes():
        wt = 0
        for nbr, eattr in G.adj[node_temp].items():
            wt = wt + eattr['weight'] * math.log2(int(eattr['year']) - 2010 + 3)
        G.nodes[node_temp]['node_wtf'] = wt
        G.nodes[node_temp]['deg'] = len(G.adj[node_temp])

    data = json_graph.node_link_data(G)
    utilities.write_json(out_dir, data)

# calculate WTf of each edge
def edge_wtf_calculation(G, out_dir):
    for n1,n2 in G.edges():
        year = G.edges[n1,n2]['year']
        wtf = G.edges[n1,n2]['weight'] * tf(n1,n2, year)
        G.edges[n1,n2]['wtf'] = wtf

    data = json_graph.node_link_data(G)
    utilities.write_json(out_dir, data)
    #print("End-->", year)


def tf(a,b,year):
    tf = math.log2((int(year)-2010)+3)
    return tf


def feature_extraction(year, G_addr):
    if year != 2012:
        G_train_address = os.path.join(G_addr, str(year)+"/train/Graph.json")
        G_test_address_previous = os.path.join(G_addr, str(year-1) + "/test/Graph.json")
    else:
        G_train_address = G_addr
    g = utilities.read_json(G_train_address)
    G = json_graph.node_link_graph(g)
    #year = G_addr.split('/')[-2]
    print("Start-->", year)

    for n1, n2 in G.edges():
        CN = 0 # common neighbors
        AA = 0 # Adamic_Adar
        HP = 0 # Hup promoted Index
        HD = 0 # Hup depressed index
        JC = 0 # jaccards coefficient
        LHN = 0 # Leich-Holm
        RA = 0 # Resource Allocation Index
        SA = 0 # Salton Index
        SO = 0 # Sorenson Index

        nghbr = list(nx.common_neighbors(G, n1, n2))
        if len(list(nghbr)) == 0:
            pass
        else:
            wtf_n1 = G.nodes[n1]['node_wtf']
            wtf_n2 = G.nodes[n2]['node_wtf']
            for z in nghbr:
                wtf_z = G.nodes[z]['node_wtf']
                numenator = G.edges[n1,z]['wtf'] + G.edges[n2,z]['wtf']
                AA += numenator / math.log2(1 + wtf_z)
                CN += numenator
                HP += numenator / min(wtf_n1, wtf_n2)
                HD += numenator / max(wtf_n1, wtf_n2)
                JC += numenator / (wtf_n1 + wtf_n2)
                LHN += numenator / (wtf_n1 * wtf_n2)
                RA += numenator / wtf_z
                SA += numenator / math.sqrt(wtf_n1 + wtf_n2)
                SO += (2 * numenator) / (wtf_n1 + wtf_n2)

        G.edges[n1,n2]['AA'] = AA
        G.edges[n1, n2]['CN'] = CN
        G.edges[n1, n2]['HP'] = HP
        G.edges[n1, n2]['HD'] = HD
        G.edges[n1, n2]['JC'] = JC
        G.edges[n1, n2]['LHN'] = LHN
        G.edges[n1, n2]['RA'] = RA
        G.edges[n1, n2]['SA'] = SA
        G.edges[n1, n2]['SO'] = SO

    data = json_graph.node_link_data(G)
    utilities.write_json(G_train_address, data)
    if year != 2012:
        utilities.write_json(G_test_address_previous, data)
    print("End-->", year)


# un-neccesary
def create_single_node_attr(root):
    G_addr = os.path.join(root, 'Graph.json')
    g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)
    for node in G.nodes:
        G.nodes[node]['single_node'] = False

    data = json_graph.node_link_data(G)
    utilities.write_json(os.path.join(G_addr), data)


# finding negative links
def non_connected_link_feature_extraction(year, root):
    if year != 2012:
        disconnect_train_addrr = os.path.join(root, str(year)+"/train/disconnect.json")
        disconnect_test_addrr = os.path.join(root, str(year-1) + "/test/disconnect.json")
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")
        G_test_address_previous = os.path.join(root, str(year - 1) + "/test/Graph.json")
    else:
        disconnect_train_addrr = os.path.join(root, str(year)+"/train/disconnect.json")
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")
    #disconnection_addr = os.path.join(root, 'disconnect.json')

    g = utilities.read_json(G_train_address)
    #g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)
    keyword_list = utilities.read_json(os.path.join(root, str(year)+'/node_list.json'))
    #print(len(keyword_list))
    #year = G_addr.split('/')[-2]

    print("Start-->", year)
    disconnection = []
    for idx, key in enumerate(keyword_list):
        for i in range(idx + 1, len(keyword_list)):
            #disconnect_edge = {}
            if keyword_list[idx] not in G.nodes():
                #idx += 1
                disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                      "year": "0", "wtf": 0.0, "AA": 0.0, "CN": 0.0, "HP": 0.0,
                                      "HD": 0.0, "JC": 0.0, "LHN": 0.0, "RA": 0.0, "SA": 0.0, "SO": 0.0,
                                      "source": keyword_list[idx], "target": keyword_list[i]})
                break
            if keyword_list[i] not in G.nodes():
                disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                      "year": "0", "wtf": 0.0, "AA": 0.0, "CN": 0.0, "HP": 0.0,
                                      "HD": 0.0, "JC": 0.0, "LHN": 0.0, "RA": 0.0, "SA": 0.0, "SO": 0.0,
                                      "source": keyword_list[idx], "target": keyword_list[i]})
                continue
            if keyword_list[idx] in G.nodes() and keyword_list[i] in G.nodes():
                if not G.has_edge(keyword_list[idx], keyword_list[i]):
                    #print(year, "new")
                    n1 = keyword_list[idx]
                    n2 = keyword_list[i]
                    CN = 0
                    AA = 0
                    HP = 0
                    HD = 0
                    JC = 0
                    LHN = 0
                    RA = 0
                    SA = 0
                    SO = 0

                    nghbr = list(nx.common_neighbors(G, n1, n2))
                    if len(list(nghbr)) == 0:
                        pass
                    else:
                        wtf_n1 = G.nodes[n1]['node_wtf']
                        a = G.nodes[n1]['deg']
                        wtf_n2 = G.nodes[n2]['node_wtf']
                        for z in nghbr:
                            #if G.nodes[z]['single_node']:
                                # print(z)
                                #continue
                            wtf_z = G.nodes[z]['node_wtf']
                            nominator = G.edges[n1, z]['wtf'] + G.edges[n2, z]['wtf']
                            AA += nominator / math.log2(1 + wtf_z)
                            CN += nominator
                            HP += nominator / min(wtf_n1, wtf_n2)
                            HD += nominator / max(wtf_n1, wtf_n2)
                            JC += nominator / (wtf_n1 + wtf_n2)
                            LHN += nominator / (wtf_n1 * wtf_n2)
                            RA += nominator / wtf_z
                            SA += nominator / math.sqrt(wtf_n1 + wtf_n2)
                            SO += (2 * nominator) / (wtf_n1 + wtf_n2)
                    disconnection.append({"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                          "year": "0", "wtf": 0.0, "AA": AA, "CN": CN,
                                          "HP": HP, "HD": HD, "JC": JC, "LHN": LHN, "RA": RA,
                                          "SA": SA, "SO": SO, "source": keyword_list[idx], "target": keyword_list[i]})
                    #print(len(disconnection))

    utilities.write_json(disconnect_train_addrr, disconnection)
    if year != 2012:
        utilities.write_json(disconnect_test_addrr, disconnection)

    print("End-->", year)

    """max_api_id = len(G.nodes()) + 1
    for idx, key in enumerate(keyword_list):
        for i in range(idx + 1, len(keyword_list)):
            print(key, keyword_list[i])
            if key == 'zoom' and keyword_list[i] == 'Transition':
                print("stop")
            single_node = False
            if keyword_list[idx] not in G.nodes():
                G.add_nodes_from([(keyword_list[idx], {"api_id": max_api_id, "node_weight": 0.0, "ratio": 0.0,
                                                       "correct_ratio": 0.0, "node_wtf": 0.0, "deg": 0.0,
                                                       "single_node": True, "id": keyword_list[idx]})])
                max_api_id += 1
                single_node = True
            if keyword_list[i] not in G.nodes():
                G.add_nodes_from([(keyword_list[idx], {"api_id": max_api_id, "node_weight": 0.0, "ratio": 0.0,
                                                       "correct_ratio": 0.0, "node_wtf": 0.0, "deg": 0.0,
                                                       "single_node": True, "id": keyword_list[i]})])
                max_api_id += 1
                single_node = True
            if single_node:
                G.add_edges_from\
                    ([(keyword_list[idx], keyword_list[i], {"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                                            "year": "0", "wtf": 0.0, "AA": 0.0, "CN": 0.0, "HP": 0.0,
                                                            "HD": 0.0, "JC": 0.0, "LHN": 0.0, "RA": 0.0, "SA": 0.0,
                                                            "SO": 0.0})])
            if not single_node:
                if G.nodes[keyword_list[idx]]['single_node']:
                    idx += 1
                    break
                if G.nodes[keyword_list[i]]['single_node']:
                    print(a)
                    continue
                else:
                    n1 = keyword_list[idx]
                    n2 = keyword_list[i]
                    CN = 0
                    AA = 0
                    HP = 0
                    HD = 0
                    JC = 0
                    LHN = 0
                    RA = 0
                    SA = 0
                    SO = 0

                    nghbr = list(nx.common_neighbors(G, n1, n2))
                    if len(list(nghbr)) == 0:
                        pass
                    else:
                        wtf_n1 = G.nodes[n1]['node_wtf']
                        a= G.nodes[n1]['deg']
                        wtf_n2 = G.nodes[n2]['node_wtf']
                        for z in nghbr:
                            if G.nodes[z]['single_node']:
                                #print(z)
                                continue
                            wtf_z = G.nodes[z]['node_wtf']
                            nominator = G.edges[n1, z]['wtf'] + G.edges[n2, z]['wtf']
                            AA += nominator / math.log2(1 + wtf_z)
                            CN += nominator
                            HP += nominator / min(wtf_n1, wtf_n2)
                            HD += nominator / max(wtf_n1, wtf_n2)
                            JC += nominator / (wtf_n1 + wtf_n2)
                            LHN += nominator / (wtf_n1 * wtf_n2)
                            RA += nominator / wtf_z
                            SA += nominator / math.sqrt(wtf_n1 + wtf_n2)
                            SO += (2 * nominator) / (wtf_n1 + wtf_n2)

                    G.add_edges_from \
                        ([(keyword_list[idx], keyword_list[i], {"weight": 0.0, "ratio": 0.0, "correct_ratio": 0.0,
                                                                "year": "0", "wtf": 0.0, "AA": AA, "CN": CN,
                                                                "HP": HP, "HD": HD, "JC": JC, "LHN": LHN, "RA": RA,
                                                                "SA": SA, "SO": SO})])

    data = json_graph.node_link_data(G)
    utilities.write_json(os.path.join(G_addr), data)
    print("End-->", year)"""


# create dataframe for training and testing data
def DataFrame_creation(year, root):
    if year != 2012:
        disconnect_train_addrr = os.path.join(root, str(year) + "/train/disconnect.json")
        disconnect_test_addrr = os.path.join(root, str(year - 1) + "/test/disconnect.json")
        disconnection = utilities.read_json(disconnect_train_addrr)
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")
        G_test_address_previous = os.path.join(root, str(year - 1) + "/test/Graph.json")
    else:
        disconnect_train_addrr = os.path.join(root, str(year) + "/train/disconnect.json")
        disconnection = utilities.read_json(disconnect_train_addrr)
        G_train_address = os.path.join(root, str(year) + "/train/Graph.json")

    g = utilities.read_json(G_train_address)
    G = json_graph.node_link_graph(g)

    ground_label_addr = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(int(year) - 1) + "/Graph.json"
    ground_label_g = utilities.read_json(ground_label_addr)
    ground_label_graph = json_graph.node_link_graph(ground_label_g)
    print("Start-->", year)

    dataset_features = ['e1', 'e2', 'Wtf', 'W', 'CN', 'AA', 'HP', 'HD', 'JC', 'LHN', 'RA', 'SA', 'SO', 'ratio',
                        'deg_e1', 'deg_e2', 'e1_ratio', 'et_ratio']
    records = []
    """for e1, e2 in G.edges():
        if ground_label_graph.has_edge(e1, e2):
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 1})
        else:
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 0})

    for non_link in disconnection:
        if ground_label_graph.has_edge(non_link['source'], non_link['target']):
            records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                            'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'], 'HP': non_link['HP'],
                            'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'], 'RA': non_link['RA'],
                            'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                            'label': 1})
        else:
            records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                            'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'], 'HP': non_link['HP'],
                            'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'], 'RA': non_link['RA'],
                            'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                            'label': 0})"""

    # check all edges in ground_label_graph
    for e1, e2 in ground_label_graph.edges():
        if G.has_edge(e1, e2):
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 1})
        else:
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': 0,
                            'W': 0, 'CN': 0,
                            'AA': 0, 'HP': 0,
                            'HD': 0, 'JC': 0,
                            'LHN': 0, 'RA': 0,
                            'SA': 0, 'SO': 0,
                            'deg_e1': 0, 'deg_e2': 0,
                            'label': 1})
    # check edges that exists in train bit not in ground_label_graph, the label
    # should be zero, but the features should be extracted from train
    for e1, e2 in G.edges():
        if not ground_label_graph.has_edge(e1, e2):
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': G.edges[e1, e2]['wtf'],
                            'W': G.edges[e1, e2]['weight'], 'CN': G.edges[e1, e2]['CN'],
                            'AA': G.edges[e1, e2]['AA'], 'HP': G.edges[e1, e2]['HP'],
                            'HD': G.edges[e1, e2]['HD'], 'JC': G.edges[e1, e2]['JC'],
                            'LHN': G.edges[e1, e2]['LHN'], 'RA': G.edges[e1, e2]['RA'],
                            'SA': G.edges[e1, e2]['RA'], 'SO': G.edges[e1, e2]['SO'],
                            'deg_e1': G.nodes[e1]['deg'], 'deg_e2': G.nodes[e2]['deg'],
                            'label': 0})
    """### disconnect
    for e1, e2 in ground_label_graph.edges():
        e1e2 = False
        for non_link in disconnection:
            if (non_link['source'] == e1 and non_link['target'] == e2) or (
                    non_link['source'] == e2 and non_link['target'] == e1):
                records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                                'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'],
                                'HP': non_link['HP'],
                                'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'],
                                'RA': non_link['RA'],
                                'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                                'label': 1})
                e1e2 = True

        if not e1e2:
            records.append({'e1': e1, 'e2': e2, 'edge_wtf': 0,
                            'W': 0, 'CN': 0, 'AA': 0, 'HP': 0,
                            'HD': 0, 'JC': 0, 'LHN': 0, 'RA': 0,
                            'SA': 0, 'SO': 0, 'deg_e1': 0, 'deg_e2': 0,
                            'label': 1})

    for non_link in disconnection:
        if not ground_label_graph.has_edge(non_link['source'], non_link['target']):
            records.append({'e1': non_link['source'], 'e2': non_link['target'], 'edge_wtf': non_link['wtf'],
                            'W': non_link['weight'], 'CN': non_link['CN'], 'AA': non_link['AA'], 'HP': non_link['HP'],
                            'HD': non_link['HD'], 'JC': non_link['JC'], 'LHN': non_link['LHN'], 'RA': non_link['RA'],
                            'SA': non_link['RA'], 'SO': non_link['SO'], 'deg_e1': 0, 'deg_e2': 0,
                            'label': 0})"""



    df = pd.DataFrame(records)
    df.to_csv(os.path.join(root, str(year) + '/train/dataframe.csv'), index=False)
    if year != 2012:
        df.to_csv(os.path.join(root, str(year - 1) + '/test/dataframe.csv'), index=False)
    print("End, df-->", year)


def main():
    # 1. extract unique apis:
    years = np.arange(2020, 2021, 1)

    """for year in years:
        keyword_list_current = utilities.read_json(
            "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year) + "/node_list.json")
        api_features_future = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(year + 1) + "/api_features"
        completed_keyword = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year + 1)
        extract_combined_apis(keyword_list_current, api_features_future, completed_keyword)"""

    # 2. combine graphs
    """for year in years:
        first_graph = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(
                year) + "/train/Graph.json"))  # combination of graphs before year of second_graph
        second_graph = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(int(year)-1) + "/Graph.json"))
        root_dir_test = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year) + "/test/Graph.json"
        root_dir_train = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year +1) + "/train/Graph.json"

        combined_graphs_edges(first_graph, second_graph, root_dir_test, root_dir_train, year)"""

    # 3. calculate sum of nodes' weight and degree
    """for year in years:
        print("NODE")
        print("Star_train -->", year)
        graph_train = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(
                year) + "/train/Graph.json"))
        graph_address_train = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year) + "/train/Graph.json"
        node_wtf_degree_calculation(graph_train, graph_address_train)
        print("End_train -->", year)
        print("Star_test -->", year)
        graph_test = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(
                year) + "/test/Graph.json"))
        graph_address_test = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year) + "/test/Graph.json"
        node_wtf_degree_calculation(graph_test, graph_address_test)
        print("End_test -->", year)"""

    # 4. calculate wtf of edges
    """for year in years:
        print("Edge")
        print("Star_train -->", year)
        graph_train = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(
                year) + "/train/Graph.json"))
        graph_address_train = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year) + "/train/Graph.json"
        edge_wtf_calculation(graph_train, graph_address_train)
        print("End_train -->", year)
        print("Star_test -->", year)
        graph_test = json_graph.node_link_graph(
            utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(
                year) + "/test/Graph.json"))
        graph_address_test = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/" + str(year) + "/test/Graph.json"
        edge_wtf_calculation(graph_test, graph_address_test)
        print("End_test -->", year)"""

    # 5. Feature Extraction
    """graph_2012_train = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/2012/train/Graph.json"
    feature_extraction(2012, graph_2012_train)"""

    """cpu_to_relax = 3
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    g_addrr = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/"
    results = pool.starmap(feature_extraction, zip(years, itertools.repeat(g_addrr)))
    pool.close()
    pool.join()"""


    # 6. create_single_node_attr
    """root_dir = []
    for year in years:
        root_dir.append("/home/c6/Desktop/OpenWPM/jsons/Prediction_new/" + str(year))

    for root in root_dir:
    # create_single_node_attr(root)"""

    # 7. non_connected_link_feature_extraction
    """root_12 = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/"
    non_connected_link_feature_extraction(2012, root_12)"""

    """cpu_to_relax = 3
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    g_addrr = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/"
    results = pool.starmap(non_connected_link_feature_extraction, zip(years, itertools.repeat(g_addrr)))
    pool.close()
    pool.join()"""


    # 8. Make DataFrame
    root_12 = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/"
    DataFrame_creation(2012, root_12)

    """cpu_to_relax = 4
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    g_addrr = "/home/c6/Desktop/OpenWPM/jsons/Prediction_new/WT/"
    #DataFrame_creation(2016, g_addrr)
    results = pool.starmap(DataFrame_creation, zip(years, itertools.repeat(g_addrr)))
    pool.close()
    pool.join()"""



if __name__ == '__main__':
    main()

