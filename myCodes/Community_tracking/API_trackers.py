from myCodes.AST import utilities
import numpy as np
import os

flagged_comm = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/2019/C_7_1")
comm_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
years = np.arange(2010,2021,1)
year = 2019
fp_api_tracks = {}

for fp_api in flagged_comm:
    year = 2019
    while year > 2009:
        static_comm_dir = os.path.join(comm_dir, str(year))
        static_comms = utilities.get_files_in_a_directory(static_comm_dir)
        for static_comm in static_comms:
            if static_comm.split('/')[-1].startswith("C_"):
                static_comm_content = utilities.read_json(static_comm)
                if fp_api in static_comm_content:
                    if fp_api not in fp_api_tracks.keys():
                        fp_api_tracks[fp_api] = [(year, static_comm.split("/")[-1])]
                    else:
                        fp_api_tracks[fp_api].append((year, static_comm.split("/")[-1]))
        year -= 1


utilities.write_json(os.path.join(comm_dir, "fp_api_tracks.json"), fp_api_tracks)


