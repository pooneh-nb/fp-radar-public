from myCodes.AST import utilities


def create_temporal_nodes():
    list_of_apis = utilities.read_file_newline_stripped("/home/c6/Desktop/OpenWPM/myCodes/AST/jsons/cleaned_apis_unique.txt")
    # get the list of nodes in each snapshot 2016-2020
    nodes_in_2016_snapshot = dict(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2016/nodes_tuple.json")).keys()
    nodes_in_2017_snapshot = dict(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2017/nodes_tuple.json")).keys()
    #nodes_in_2018_snapshot = dict(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2018/nodes_tuple.json")).keys()
    #nodes_in_2019_snapshot = dict(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2019/nodes_tuple.json")).keys()
    #nodes_in_2020_snapshot = dict(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2020/nodes_tuple.json")).keys()

    # Create one node per api per point in time.
    nodes_temporal_set = {}
    for api_k in list_of_apis:
        time_stamps = []
        if api_k in nodes_in_2016_snapshot:
            time_stamps.append(2016)
        if api_k in nodes_in_2017_snapshot:
            time_stamps.append(2017)
        """if api_k in nodes_in_2018_snapshot:
            time_stamps.append(2018)
        if api_k in nodes_in_2019_snapshot:
            time_stamps.append(2019)
        if api_k in nodes_in_2020_snapshot:
            time_stamps.append(2020)"""
        if len(time_stamps) != 0:
            nodes_temporal_set[api_k] = sorted(time_stamps)

def create_temporal_edge():
    pass



