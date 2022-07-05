import networkx as nx
import matplotlib.pyplot as plt
import json
import math
from networkx.readwrite import json_graph
from myCodes.AST import utilities
import community as community_louvain
import pandas as pd
import numpy as np
import os

summary_result = []


# Create and load Graph
def load_graph(graph_dir):
    G_addr = graph_dir
    g = utilities.read_json(G_addr)
    G = json_graph.node_link_graph(g)

    # add node degree and weight
    for node_temp in G.nodes():
        wt = 0
        deg = 0
        for nbr, eattr in G.adj[node_temp].items():
            wt = wt + eattr['weight']
            deg += 1
        G.nodes[node_temp]['deg_wt'] = wt
        G.nodes[node_temp]['deg'] = deg

    return G


# basic information
def basic_information(year, G):
    print("Year --> ", year)
    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    print("Number of Nodes: ", num_nodes)
    print("Number of Edges: ", num_edges)

    degree_freq = []  # degree
    pure_count = 0  # pure FP API
    high_ratio_count = 0
    for nod in G.nodes:
        # degree
        degree_freq.append(G.nodes[nod]['deg'])
        # pure fp API
        if G.nodes[nod]['ratio'] == 'i':
            pure_count += 1
        # ratio > 16
        if G.nodes[nod]['ratio'] != 'i':
            if G.nodes[nod]['ratio'] > 16:
                high_ratio_count += 1

    # Degree Report
    avg_deg = sum(degree_freq) / len(G.nodes)
    min_deg = min(degree_freq)
    max_deg = max(degree_freq)
    print("Average Degree: ", avg_deg)
    print("minimum Degree: ", min_deg)
    print("maximum Degree: ", max_deg)

    summary_result.append({"Year": year,
                           "#Nodes": num_nodes,
                           "#Edges": num_edges,
                           "Avg_deg": avg_deg,
                           "min_deg": min_deg,
                           "max_deg": max_deg,
                           "#pure_fp_API": pure_count,
                           "#high_ratio_API": high_ratio_count
                           })

    summary_df = pd.DataFrame(summary_result)
    return summary_df


# Lovain method
def lovain_method(G, out_dir):
    total_comm = 0
    partition = community_louvain.best_partition(G, resolution=0.91, weight='weight')
    num_of_partitions = len(set(partition.values()))
    total_comm += num_of_partitions
    print("partitions: ", num_of_partitions)

    louvain_clusters = {}
    for i in range(num_of_partitions):
        clust = []
        for key, value in partition.items():
            if value == i:
                clust.append(key)
        louvain_clusters[i] = clust

        # sub-clustering
        if len(louvain_clusters[i]) > 0.3 * len(G.nodes()):
            partition2 = community_louvain.best_partition(G.subgraph(louvain_clusters[i]), resolution=0.91,
                                                          weight='weight')
            num_of_partitions2 = len(set(partition2.values()))
            total_comm += num_of_partitions2 - 1
            print("Sub_partitions: ", num_of_partitions2)

            louvain_clusters2 = {}
            for j in range(num_of_partitions2):
                clust2 = []
                for key, value in partition2.items():
                    if value == j:
                        clust2.append(key)
                louvain_clusters2[j] = clust2
                utilities.write_json(os.path.join(out_dir, 'C_' + str(i) + '_' + str(j)), louvain_clusters2[j])

        else:
            utilities.write_json(os.path.join(out_dir, 'C_' + str(i)), louvain_clusters[i])

    return total_comm


def write_length_of_communities(communities_dir, total_nodes):
    readme = []
    communities = utilities.get_files_in_a_directory(communities_dir)

    for community in communities:
        com_name = community.split('/')[-1]
        if not com_name.startswith("C_"):
            continue
        com = utilities.read_json(community)
        readme.append({com_name: len(com)})
        print(com_name, len(com))
        # sub_clustering

    utilities.write_json(os.path.join(communities_dir, "readme.json"), readme)


# report the status of pure, >16, and fpjs2 APIs
def cluster_analysis(communities_dir, G):
    communities = utilities.get_files_in_a_directory(communities_dir)
    records = []

    with open("/home/c6/Desktop/OpenWPM/myCodes/AST/jsons/fingerprinting_js2.txt", 'r') as file:
        bench_lib = file.read().splitlines()

    for comm in communities:
        comm_context = utilities.read_json(comm)
        comm_name = comm.split('/')[-1]
        if not comm_name.startswith("C_"):
            continue
        fp_api = 0
        fpjs2 = 0
        pure_fp_api = 0

        for api in comm_context:
            if G.nodes[api]['ratio'] == 'i':
                pure_fp_api += 1
            if G.nodes[api]['ratio'] != 'i':
                if G.nodes[api]['ratio'] > 16:
                    fp_api += 1
            if api in bench_lib:
                fpjs2 += 1

        records.append({"cluster": comm_name,
                        "fpjs2": fpjs2,
                        "pure": pure_fp_api,
                        "ratio_16": fp_api,
                        "len": len(comm_context)})

    df_records = pd.DataFrame(records)
    print(df_records)
    utilities.write_json(os.path.join(communities_dir, "comm_report.json"), records)


def main():
    years = np.arange(2010, 2020, 1)
    partition_counter = []
    for year in years:
        real_comm_addr = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/" + str(year)

        # load graph
        graph = load_graph("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/" + str(year) + "/Graph.json")

        # read basic information
        df = basic_information(year, graph)

        # call Louvain method
        for i in range(1):
            num_partition = lovain_method(graph, real_comm_addr)
            print(num_partition)
        partition_counter.append(num_partition)
        df["#partitions"] = partition_counter

        # create readme for length of clusters
        write_length_of_communities(real_comm_addr, len(graph.nodes()))

        # cluster analysing
        cluster_analysis(real_comm_addr, graph)
        print(df)
    df.to_csv("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/summery_report.csv", index=False)


if __name__ == '__main__':
    main()

trackr_radar_weights = {key: value for key, value in
                        sorted(trackr_radar_weights_dict.items(), key=lambda item: item[1], reverse=True)}
