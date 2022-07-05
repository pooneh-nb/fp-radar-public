from myCodes.AST import utilities
import os

base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs/DY_COMM"
selected_dynamic_communities = utilities.read_json(
        os.path.join(base_dir, "selected_comms/selected_DY_communities.json"))

fp_ststic_clusters = utilities.read_json()