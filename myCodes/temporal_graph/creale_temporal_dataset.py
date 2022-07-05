from myCodes.AST import utilities
import pandas as pd


def create_ref_api_dict():
    ref_api_list = utilities.read_file("/home/c6/Desktop/OpenWPM/myCodes/AST/jsons/cleaned_apis_unique.txt")
    ref_api_dict = {}

    api_id = 1
    for api in ref_api_list:
        ref_api_dict[api.split('\n')[0]] = api_id
        api_id += 1

    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/reference_api.json", ref_api_dict)


def create_pruned_temporal_graph_dict():
    nodes_2020 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2020/nodes_tuple.json")
    nodes_2019 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2019/nodes_tuple.json")
    nodes_2018 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2018/nodes_tuple.json")
    nodes_2017 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2017/nodes_tuple.json")
    nodes_2016 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2016/nodes_tuple.json")
    zero_day_fp = set()
    for item in nodes_2020:
        if item[1]['node_weight'] > 2:
            zero_day_fp.add(item[0])

    for item in nodes_2019:
        if item[1]['node_weight'] > 2:
            zero_day_fp.add(item[0])

    for item in nodes_2018:
        if item[1]['node_weight'] > 2:
            zero_day_fp.add(item[0])

    for item in nodes_2017:
        if item[1]['node_weight'] > 2:
            zero_day_fp.add(item[0])

    for item in nodes_2016:
        if item[1]['node_weight'] > 2:
            zero_day_fp.add(item[0])
    reference_api = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/reference_api.json")
    edge_tuple_2020 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2020/edges_tuple.json")
    edge_tuple_2019 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2019/edges_tuple.json")
    edge_tuple_2018 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2018/edges_tuple.json")
    edge_tuple_2017 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2017/edges_tuple.json")
    edge_tuple_2016 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2016/edges_tuple.json")

    keyDict = {"u", "v", "t"}
    temporal_dict = dict([(key, []) for key in keyDict])
    #temporal_dict = {}
    for edge_tup in edge_tuple_2020:
        if edge_tup[2]['weight'] > 0:
            if edge_tup[0] == '\\\\n':
                edge_tup[0] = '\n'
            if edge_tup[1] == '\\\\n':
                edge_tup[1] = '\n'
            if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                temporal_dict['u'].append(reference_api[edge_tup[1]])
                temporal_dict['v'].append(reference_api[edge_tup[0]])
                temporal_dict['t'].append(2020)
            else:
                temporal_dict['u'].append(reference_api[edge_tup[0]])
                temporal_dict['v'].append(reference_api[edge_tup[1]])
                temporal_dict['t'].append(2020)
        if edge_tup[2]['weight'] < 0:
            if edge_tup[0] in zero_day_fp or edge_tup[1] in zero_day_fp:
                if edge_tup[0] == '\\\\n':
                    edge_tup[0] = '\n'
                if edge_tup[1] == '\\\\n':
                    edge_tup[1] = '\n'
                if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                    temporal_dict['u'].append(reference_api[edge_tup[1]])
                    temporal_dict['v'].append(reference_api[edge_tup[0]])
                    temporal_dict['t'].append(2020)
                else:
                    temporal_dict['u'].append(reference_api[edge_tup[0]])
                    temporal_dict['v'].append(reference_api[edge_tup[1]])
                    temporal_dict['t'].append(2020)

    for edge_tup in edge_tuple_2019:
        if edge_tup[2]['weight'] > 0:
            if edge_tup[0] == '\\\\n':
                edge_tup[0] = '\n'
            if edge_tup[1] == '\\\\n':
                edge_tup[1] = '\n'
            if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                temporal_dict['u'].append(reference_api[edge_tup[1]])
                temporal_dict['v'].append(reference_api[edge_tup[0]])
                temporal_dict['t'].append(2019)
            else:
                temporal_dict['u'].append(reference_api[edge_tup[0]])
                temporal_dict['v'].append(reference_api[edge_tup[1]])
                temporal_dict['t'].append(2019)
        if edge_tup[2]['weight'] < 0:
            if edge_tup[0] in zero_day_fp or edge_tup[1] in zero_day_fp:
                if edge_tup[0] == '\\\\n':
                    edge_tup[0] = '\n'
                if edge_tup[1] == '\\\\n':
                    edge_tup[1] = '\n'
                if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                    temporal_dict['u'].append(reference_api[edge_tup[1]])
                    temporal_dict['v'].append(reference_api[edge_tup[0]])
                    temporal_dict['t'].append(2019)
                else:
                    temporal_dict['u'].append(reference_api[edge_tup[0]])
                    temporal_dict['v'].append(reference_api[edge_tup[1]])
                    temporal_dict['t'].append(2019)

    for edge_tup in edge_tuple_2018:
        if edge_tup[2]['weight'] > 0:
            if edge_tup[0] == '\\n':
                edge_tup[0] = '\n'
            if edge_tup[1] == '\\n':
                edge_tup[1] = '\n'
            if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                temporal_dict['u'].append(reference_api[edge_tup[1]])
                temporal_dict['v'].append(reference_api[edge_tup[0]])
                temporal_dict['t'].append(2018)
            else:
                temporal_dict['u'].append(reference_api[edge_tup[0]])
                temporal_dict['v'].append(reference_api[edge_tup[1]])
                temporal_dict['t'].append(2018)
        if edge_tup[2]['weight'] < 0:
            if edge_tup[0] in zero_day_fp or edge_tup[1] in zero_day_fp:
                if edge_tup[0] == '\\n':
                    edge_tup[0] = '\n'
                if edge_tup[1] == '\\n':
                    edge_tup[1] = '\n'
                if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                    temporal_dict['u'].append(reference_api[edge_tup[1]])
                    temporal_dict['v'].append(reference_api[edge_tup[0]])
                    temporal_dict['t'].append(2018)
                else:
                    temporal_dict['u'].append(reference_api[edge_tup[0]])
                    temporal_dict['v'].append(reference_api[edge_tup[1]])
                    temporal_dict['t'].append(2018)

    for edge_tup in edge_tuple_2017:
        if edge_tup[2]['weight'] > 0:
            if edge_tup[0] == '\\n':
                edge_tup[0] = '\n'
            if edge_tup[1] == '\\n':
                edge_tup[1] = '\n'
            if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                temporal_dict['u'].append(reference_api[edge_tup[1]])
                temporal_dict['v'].append(reference_api[edge_tup[0]])
                temporal_dict['t'].append(2017)
            else:
                temporal_dict['u'].append(reference_api[edge_tup[0]])
                temporal_dict['v'].append(reference_api[edge_tup[1]])
                temporal_dict['t'].append(2017)
        if edge_tup[2]['weight'] < 0:
            if edge_tup[0] in zero_day_fp or edge_tup[1] in zero_day_fp:
                if edge_tup[0] == '\\n':
                    edge_tup[0] = '\n'
                if edge_tup[1] == '\\n':
                    edge_tup[1] = '\n'
                if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                    temporal_dict['u'].append(reference_api[edge_tup[1]])
                    temporal_dict['v'].append(reference_api[edge_tup[0]])
                    temporal_dict['t'].append(2017)
                else:
                    temporal_dict['u'].append(reference_api[edge_tup[0]])
                    temporal_dict['v'].append(reference_api[edge_tup[1]])
                    temporal_dict['t'].append(2017)

    for edge_tup in edge_tuple_2016:
        if edge_tup[2]['weight'] > 0:
            if edge_tup[0] == '\\n':
                edge_tup[0] = '\n'
            if edge_tup[1] == '\\n':
                edge_tup[1] = '\n'
            if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                temporal_dict['u'].append(reference_api[edge_tup[1]])
                temporal_dict['v'].append(reference_api[edge_tup[0]])
                temporal_dict['t'].append(2016)
            else:
                temporal_dict['u'].append(reference_api[edge_tup[0]])
                temporal_dict['v'].append(reference_api[edge_tup[1]])
                temporal_dict['t'].append(2016)
        if edge_tup[2]['weight'] < 0:
            if edge_tup[0] in zero_day_fp or edge_tup[1] in zero_day_fp:
                if edge_tup[0] == '\\n':
                    edge_tup[0] = '\n'
                if edge_tup[1] == '\\n':
                    edge_tup[1] = '\n'
                if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
                    temporal_dict['u'].append(reference_api[edge_tup[1]])
                    temporal_dict['v'].append(reference_api[edge_tup[0]])
                    temporal_dict['t'].append(2016)
                else:
                    temporal_dict['u'].append(reference_api[edge_tup[0]])
                    temporal_dict['v'].append(reference_api[edge_tup[1]])
                    temporal_dict['t'].append(2016)

    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/pruned_temporal_edge.json", temporal_dict)


def temporal_2020():
    reference_api = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/reference_api.json")
    edge_tuple_2016 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2020/edges_tuple.json")
    keyDict = {"u", "v", "w"}
    temporal_dict = dict([(key, []) for key in keyDict])

    for edge_tup in edge_tuple_2016:
        if edge_tup[0] == '\\\\n':
            edge_tup[0] = '\n'
        if edge_tup[1] == '\\\\n':
            edge_tup[1] = '\n'
        if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
            temporal_dict['u'].append(reference_api[edge_tup[1]])
            temporal_dict['v'].append(reference_api[edge_tup[0]])
            #temporal_dict['t'].append(2015)
            temporal_dict['w'].append(edge_tup[2]['weight'])
        else:
            temporal_dict['u'].append(reference_api[edge_tup[0]])
            temporal_dict['v'].append(reference_api[edge_tup[1]])
            #temporal_dict['t'].append(2015)
            temporal_dict['w'].append(edge_tup[2]['weight'])
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/temporal_2020.json", temporal_dict)

def create_temporal_graph_dict():
    reference_api = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/reference_api.json")
    edge_tuple_2020 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2020/edges_tuple.json")
    edge_tuple_2019 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2019/edges_tuple.json")
    edge_tuple_2018 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2018/edges_tuple.json")
    edge_tuple_2017 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2017/edges_tuple.json")
    edge_tuple_2016 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/2016/edges_tuple.json")
    keyDict = {"u", "v", "t", "w"}
    temporal_dict = dict([(key, []) for key in keyDict])

    for edge_tup in edge_tuple_2020:
        if edge_tup[0] == '\\\\n':
            edge_tup[0] = '\n'
        if edge_tup[1] == '\\\\n':
            edge_tup[1] = '\n'
        if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
            temporal_dict['u'].append(reference_api[edge_tup[1]])
            temporal_dict['v'].append(reference_api[edge_tup[0]])
            temporal_dict['t'].append(2020)
            temporal_dict['w'].append(edge_tup[2]['weight'])
        else:
            temporal_dict['u'].append(reference_api[edge_tup[0]])
            temporal_dict['v'].append(reference_api[edge_tup[1]])
            temporal_dict['t'].append(2020)
            temporal_dict['w'].append(edge_tup[2]['weight'])

    for edge_tup in edge_tuple_2019:
        if edge_tup[0] == '\\\\n':
            edge_tup[0] = '\n'
        if edge_tup[1] == '\\\\n':
            edge_tup[1] = '\n'
        if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
            temporal_dict['u'].append(reference_api[edge_tup[1]])
            temporal_dict['v'].append(reference_api[edge_tup[0]])
            temporal_dict['t'].append(2019)
            temporal_dict['w'].append(edge_tup[2]['weight'])
        else:
            temporal_dict['u'].append(reference_api[edge_tup[0]])
            temporal_dict['v'].append(reference_api[edge_tup[1]])
            temporal_dict['t'].append(2019)
            temporal_dict['w'].append(edge_tup[2]['weight'])

    for edge_tup in edge_tuple_2018:
        if edge_tup[0] == '\\n':
            edge_tup[0] = '\n'
        if edge_tup[1] == '\\n':
            edge_tup[1] = '\n'
        if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
            temporal_dict['u'].append(reference_api[edge_tup[1]])
            temporal_dict['v'].append(reference_api[edge_tup[0]])
            temporal_dict['t'].append(2018)
            temporal_dict['w'].append(edge_tup[2]['weight'])
        else:
            temporal_dict['u'].append(reference_api[edge_tup[0]])
            temporal_dict['v'].append(reference_api[edge_tup[1]])
            temporal_dict['t'].append(2018)
            temporal_dict['w'].append(edge_tup[2]['weight'])

    for edge_tup in edge_tuple_2017:
        if edge_tup[0] == '\\n':
            edge_tup[0] = '\n'
        if edge_tup[1] == '\\n':
            edge_tup[1] = '\n'
        if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
            temporal_dict['u'].append(reference_api[edge_tup[1]])
            temporal_dict['v'].append(reference_api[edge_tup[0]])
            temporal_dict['t'].append(2017)
            temporal_dict['w'].append(edge_tup[2]['weight'])
        else:
            temporal_dict['u'].append(reference_api[edge_tup[0]])
            temporal_dict['v'].append(reference_api[edge_tup[1]])
            temporal_dict['t'].append(2017)
            temporal_dict['w'].append(edge_tup[2]['weight'])

    for edge_tup in edge_tuple_2016:
        if edge_tup[0] == '\\n':
            edge_tup[0] = '\n'
        if edge_tup[1] == '\\n':
            edge_tup[1] = '\n'
        if reference_api[edge_tup[0]] < reference_api[edge_tup[1]]:
            temporal_dict['u'].append(reference_api[edge_tup[1]])
            temporal_dict['v'].append(reference_api[edge_tup[0]])
            temporal_dict['t'].append(2016)
            temporal_dict['w'].append(edge_tup[2]['weight'])
        else:
            temporal_dict['u'].append(reference_api[edge_tup[0]])
            temporal_dict['v'].append(reference_api[edge_tup[1]])
            temporal_dict['t'].append(2016)
            temporal_dict['w'].append(edge_tup[2]['weight'])

    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/temporal_weighted_edge.json", temporal_dict)


def create_temporal_dataframe():
    temporal_dict = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/temporal_2020.json")
    df = pd.DataFrame(data=temporal_dict, columns=['u', 'v','w'])
    #print("Original DataFrame")
    #print(df)
    #print('Data from new_file.csv file:')
    df.to_csv('/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/temporal_2020.csv', sep='\t', index=False)
    #new_df = pd.read_csv('/home/c6/Desktop/OpenWPM/jsons/temporal_graphs/temporal_df_2015.csv')
    #print(new_df)


#create_temporal_graph_dict()
#temporal_2020()
create_temporal_dataframe()