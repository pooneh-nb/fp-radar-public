from myCodes.AST import utilities
import os


def setify_class_members(class_api, outdir):
    # function: take the list of each class and convert them to set to get rid of repetitive members
    class_api_copy = {}
    for class_name, member_list in class_api.items():
        member_list = [each_string.lower() for each_string in member_list]
        class_api_copy[class_name] = list(set(member_list))
    utilities.write_json(os.path.join(outdir,"class_api.json"), class_api_copy)


def setify_api_class(api_class, labeling_cluster_dir):
    # function: take the list of each api and convert them to set to get rid of repetitive members
    api_class_copy = {}
    ## normalize key names
    for api_name, member_list in api_class.items():
        #print(api_name)
        api_name_normalized = api_name.lower()
        if api_name_normalized not in api_class_copy.keys():
            member_list = [each_string.lower() for each_string in member_list]
            api_class_copy[api_name_normalized] = list(set(member_list))
        else:
            member_list = set([each_string.lower() for each_string in member_list])
            for mem in member_list:
                api_class_copy[api_name_normalized].append(mem)
    print("setidy")

    ## setify
    api_class_copy2 = {}
    for api_name, member_list in api_class_copy.items():
        api_class_copy2[api_name] = list(set(member_list))
    utilities.write_json(os.path.join(labeling_cluster_dir, "api_class_new.json"), api_class_copy2)


def remove_duplicate_api_members(api_class, class_api, new_class_api_adrss):
    for api, class_list in api_class.items():
        if len(class_list) > 1:
            for idx, clss in enumerate(class_list):
                for idx_next, clss_next in enumerate(class_list):
                    if idx == idx_next:
                        continue
                    if clss_next in class_api[clss]:  # if a class is subclass of another class
                        class_api[clss].remove(clss_next)
                        api_class[api].remove(clss_next)
                        for api_members in class_api[clss_next]:
                            if api_members in class_api[clss]:
                                class_api[clss].remove(api_members)
    #utilities.write_json(os.path.join(new_class_api_adrss, "class_api_new.json"), class_api)
    utilities.write_json(os.path.join(new_class_api_adrss, "api_class_new.json"), api_class)

def address_API_name_as_class(api_class, api_class_addrr):
    for api_name, clss_list in api_class.items():
        for clss in clss_list:
            if clss == "API":
                api_class[api_name].remove(clss)
                api_class[api_name].append(api_name)

    utilities.write_json(os.path.join(api_class_addrr, "api_class_copy.json"), api_class)


def selected_dynamic_community_api_class(base_communities_dir, dy_comms, static_comm_base, all_api_class):
    dy_comm_dic = {}
    for dycm_id, dymc_membr in dy_comms.items():
        dy_comm_dic[dycm_id] = {}
        for static_com in dymc_membr:
            print("start: ", dycm_id, "+", static_com)
            class_of_api = []
            api_class = {}
            for api in utilities.read_json(os.path.join(static_comm_base, str(static_com[1]), static_com[0])):
                # class_of_api = all_api_class[api]
                api_class[api] = all_api_class[api]
            dy_comm_dic[dycm_id][str((str(static_com[0]), static_com[1], static_com[2]))] = {
                "static_comm": static_com[0],
                "year": static_com[1],
                "status": static_com[2],
                "api_class": api_class
            }
        utilities.write_json(os.path.join(base_communities_dir, "real_graphs/DY_COMM/", dycm_id + ".json"), dy_comm_dic)


def frequency_of_class_in_DYcomms(selected_DYcomms):
    # function: find the frequency of each class in in each dynamic cluster
    for dyname, stat_comms in selected_DYcomms:
        class_glossary = {}
        for stat_comm in stat_comms:
            stat_name = stat_name[0]
            year = stat_comm[1]
            stat_content = utilities.read_json(os.path.join("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs",year,stat_name))


def define_major_label(selected_comms, out_dir):
    for dy_comm in selected_comms:
        class_glossary = {}
        comm_content = utilities.read_json(dy_comm)
        for dy_id, value in comm_content.items():
            for stat_coms, val in value.items():
                for api_name, class_list in val['api_class'].items():
                    if type(class_list) == list:
                        for cl in class_list:
                            if cl == 'G':
                                print("stop")
                            if cl not in class_glossary.keys():
                                class_glossary[cl] = 1
                            else:
                                class_glossary[cl] += 1
                        else:
                            if cl not in class_glossary.keys():
                                class_glossary[cl] = 1
                            else:
                                class_glossary[cl] += 1

        sorted_class_glossary = sorted(class_glossary.items(), key=lambda kv: kv[1], reverse=True)
       # utilities.write_json(os.path.join(out_dir", dy_id + ".json"),
                             #sorted_class_glossary)
        sorted_class_glossary = {}


def assign_API_to_CLass(api_class, out_dir):
    # input: api_class.json
    # output: class_api.json
    class_api = {}
    for api_keyw, class_list in api_class.items():
        for clss in class_list:
            if clss not in class_api.keys():
                class_api[clss] = []
                class_api[clss].append(api_keyw)
            else:
                class_api[clss].append(api_keyw)
    utilities.write_json(os.path.join(out_dir, "class_api.json"), class_api)


def assign_class_to_API(class_api_new, out_dir):
    # input: class_api_new.json
    # output: api_class_new.json
    api_class = {}
    for class_name, api_list in class_api_new.items():
        for api in api_list:
            if api not in api_class.keys():
                api_class[api] = []
                api_class[api].append(class_name)
            else:
                api_class[api].append(class_name)
    utilities.write_json(os.path.join(out_dir, "api_class_new.json"), api_class)

def normalize_class_wight(selected_dynm_comm, unormalized_class_weights, class_api, outdir):
    for file in unormalized_class_weights:
        dy_name = file.split('/')[-1].split('.')[0]
        if file.split('/')[-1].split('.')[-1] == "zip":
            continue
        context = dict(utilities.read_json(file))
        print(dy_name)
        if dy_name not in selected_dynm_comm.keys():
            continue
        dy_length = len(selected_dynm_comm[dy_name])
        for clss, value in context.items():
            class_name = clss
            class_unormal_weight = value
            class_member_length = len(class_api[class_name])
            normal_weight = ((class_unormal_weight/dy_length)/class_member_length) * 100
            context[clss] = round(normal_weight, 2)
        sorted_context = sorted(context.items(), key=lambda kv: kv[1], reverse=True)
        utilities.write_json(os.path.join(outdir, str(dy_name+".json")), sorted_context)


def main():
    # DIRECTORIES AND FILES
    api_class_new = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters/api_class_new.json")
    api_class = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters/api_class.json")
    class_api_new = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters/class_api_new.json")
    class_api = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters/class_api.json")
    community_tracking_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/"
    labeling_cluster_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/labeling_clusters"
    selected_dy_clusters = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/selected_comms/selected_DY_communities.json")

    # CALL FUNCTIONS

    # function: weight of each class in each static cluster of a dynamic cluster
    #### define_major_label(selected_dy_clusters, labeling_cluster_dir)



    ##!!!!!!!!!!!!!!!!!!!!!!!!!!
    # normalize_class_weights:
    #######3REMOVE
    #  input
    #####unormalized_class_weights = utilities.get_files_in_a_directory(
        #"/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/sorted_labels")
    ######outdir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM/sorted_labels/normalized"
    #####class_api = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/class_api.json")
    #  call function
    ###normalize_class_wight(selected_dynm_comm, unormalized_class_weights, class_api, outdir)
    #######!!!!!!!!!!!!!

    ### 1. remove API as class name
    # function: remove API as a class name
    # address_API_name_as_class(api_class, labeling_cluster_dir)

    ### 2. lowercase and setify members of api_class.json
    #setify_api_class(api_class, labeling_cluster_dir)

    # 3. function: assign all APIs to their clusters
    #assign_API_to_CLass(api_class, labeling_cluster_dir)

    #### 4 . lowercase and setify class members of class_api.json
    #setify_class_members(class_api, labeling_cluster_dir)

    #### 5. remove duplicate parrents
    #remove_duplicate_api_members(api_class, class_api, labeling_cluster_dir)

    ### 6. remove duplicate classes assigned to apies
    #assign_class_to_API(class_api_new, labeling_cluster_dir)


    """count_multi = 0
    count_z = 0
    for api, class_list in class_api_new.items():
        if len(class_list) > 1:
            count_multi += 1
        if len(class_list) == 0:
            count_z += 1
    print("total: ", len(class_api_new.keys()), "multi: ", count_multi, "zerp: ",count_z)"""


    print(len(api_class.keys()))
    print(len(api_class_new.keys()))



if __name__ == '__main__':
    main()
