from myCodes.AST import utilities
import os
import pandas as pd

dy_comm_addrr = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs" \
                "/DY_COMM/selected_comms/selected_DY_community_edited.json"
dy_comm_json = utilities.read_json(dy_comm_addrr)

df_cy = {'year':[], 'dy_group_name': [], 'static_grp_name': [], 'length': [], 'ranking': []}
for dy_name, comms in dy_comm_json.items():
    for key in comms:
        df_cy['year'].append(key[1])
        df_cy['dy_group_name'].append(dy_name)
        df_cy['static_grp_name'].append(key[0])
        df_cy['ranking'].append(key[3]+1)
        static_comm_addr = utilities.read_json\
            (os.path.join("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs",str(key[1]), key[0]))
        df_cy['length'].append(len(static_comm_addr))

df = pd.DataFrame(data=df_cy)
df.to_csv("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/dy_communities2.csv",sep=',')

