import json
from myCodes.AST import utilities
import os

with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/wayback_results/2020/sorted_louvian_0.88.json", "rt") as r:
    sorted_louvian = json.load(r)

with open("/home/pooneh/Desktop/OpenWPM/jsons/AST/wayback_results/2020/grouped_dict_0.88.json", "rt") as lo:
    louvain_group = json.load(lo)

with open("/home/pooneh/Desktop/OpenWPM/myCodes/AST/jsons/fingerprinting_js2.txt", 'r') as file:
    bench_lib = file.read().splitlines()

for key_group, value_api_list in louvain_group.items():
    print(key_group)
    group_content = ""
    for api in value_api_list['api_list']:
    #for api_key, api_value in value_api_list.items():
        #for api in api_value:
        file_address = os.path.join("/home/pooneh/Desktop/OpenWPM/jsons/AST/wayback_results/2020/groups", str(key_group)+'.txt')
        group_content = api + ", " + str(sorted_louvian[api]['weight']) + ", " + str(sorted_louvian[api]['script'])
        utilities.append_file(file_address, group_content)

