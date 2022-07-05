import numpy as np
import os

from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

from myCodes.AST import utilities

"""threshold=0.3
steps_to_die=3
lst_idx = 0
DY_COMMS = {}
Front = []
temp_front_new = []
temp_front_remove = []"""


class DynamicCommunityTracking:

    def __init__(self):

        self.lst_idx = 0
        self.DY_COMMS = {}
        self.Front = []
        self.temp_front_new = []
        self.temp_front_remove = []
        self.threshold = 0.1
        self.steps_to_die = 3

    def bootstrap(self, G_1):

        for comm in G_1:
            comm_name = comm.split('/')[-1]
            if not comm_name.startswith("C_"):
                continue
            time = 2010
            event = "birth"
            self.DY_COMMS[self.lst_idx] = [(comm_name, time, event)]
            self.Front.append((comm_name, time, "birth"))
            self.lst_idx += 1

    def one_to_one_match(self, communities, base_dir):
        for next_comm in communities:
            if not next_comm.split('/')[-1].startswith("C_"):
                continue
            next_comm_context = utilities.read_json(next_comm)
            unmatched = True
            for f in self.Front:
                f_comm = utilities.read_json(os.path.join(base_dir, str(f[1]), f[0]))
                if self._jaccard_coefficient(f_comm, next_comm_context) > self.threshold:
                    self._check_event_status(next_comm, f, base_dir)
                    # update_front(DY_COMMS, next_comm, Front, f, year, lst_idx, base_dir)
                    unmatched = False
                    """if process_split():
                        continue
                    elif process_merge():
                        continue
                    elif process_normal_prgress():
                        continue"""
            if unmatched:
                self._add_new_dcomm(next_comm)

    def _check_event_status(self, next_comm, f, base_dir):

        key = self._get_key(f, self.DY_COMMS)

        new_comm_name = next_comm.split('/')[-1]
        new_comm_year = int(next_comm.split('/')[-2])
        next_comm_comtext = utilities.read_json(next_comm)

        f_name = f[0]
        f_year = int(f[1])
        f_event = f[2]
        f_context = utilities.read_json(os.path.join(base_dir, str(f_year), f_name))

        if self._process_split(self.DY_COMMS[key], new_comm_name, new_comm_year):
            # should get the history of front im DY_comm
            self.DY_COMMS[self.lst_idx] = []
            for item in self.DY_COMMS[key][:-1]:
                self.DY_COMMS[self.lst_idx].append(item)
            self.DY_COMMS[self.lst_idx].append((new_comm_name, new_comm_year, "split"))
            #self._update_dy_comm(key, new_comm_name, new_comm_year, "split", f_name, f_year, f_event)
            self.lst_idx += 1
            return

        if self._process_merge(new_comm_name, new_comm_year):
            self._update_dy_comm(key, new_comm_name, new_comm_year, "merge", f_name, f_year, f_event)
            return
        else:
            ratio = len(next_comm_comtext) / len(f_context)
            if ratio > 1.1:
                event = "grow"
            elif ratio < 0.9:
                event = "contraction"
            else:
                event = "stay"
            self._update_dy_comm(key, new_comm_name, new_comm_year, event, f_name, f_year, f_event)
            return

    def _process_split(self, DY_COMMS_key, new_comm_name, new_comm_year):
        for item in DY_COMMS_key:
            if item[0] != new_comm_name and item[1] == new_comm_year:
                return True

    def _process_merge(self, new_comm_name, new_comm_year):
            #for f in self.temp_front_remove:
        for f in self.temp_front_new:
            if f[0] == new_comm_name and f[1] == new_comm_year:
                return True

    def _update_temp_front(self, rm_item, new_item):
        if rm_item == "new":
            self.temp_front_new.append(new_item)
        else:
            self.temp_front_new.append(new_item)
            self.temp_front_remove.append(rm_item)

    def update_front(self, year):
        for f_new in self.temp_front_new:
            self.Front.append(f_new)
        for f_rm in self.temp_front_remove:
            self.Front.remove(f_rm)

        self.temp_front_remove.clear()
        self.temp_front_new.clear()

    def process_death(self, year):
        for f in self.Front:
            if f == ('C_2', 2010, 'birth'):
                print("gotcha")
            if int(year) - int(f[1]) > self.steps_to_die:
                key = self._get_key(f, self.DY_COMMS)
                self.DY_COMMS[key].append((f[0], f[1], "DEAD"))
                self.Front.remove(f)


        print(self.DY_COMMS)
        print(len(self.DY_COMMS))
        print(self.Front)
        print(len(self.Front))

    def _update_dy_comm(self, key, new_comm_name, new_comm_year, event, f_name, f_year, f_event):
        self.DY_COMMS[key].append((new_comm_name, new_comm_year, event))
        self._update_temp_front((f_name, f_year, f_event), (new_comm_name, new_comm_year, event))

    def _add_new_dcomm(self, comm):
        new_comm_name = comm.split('/')[-1]
        new_comm_year = int(comm.split('/')[-2])
        self.DY_COMMS[self.lst_idx] = [(new_comm_name, new_comm_year, "birth")]
        self.lst_idx += 1
        self._update_temp_front("new", (new_comm_name, new_comm_year, "birth"))

    def _jaccard_coefficient(self, community_1, community_2) -> float:
        s1 = set(community_1)
        s2 = set(community_2)
        similarity = len(s1.intersection(s2)) / len(s1.union(s2))
        return similarity

    def _get_key(self, val, dict):
        for key, value in dict.items():
            for item in value:
                if val == item:
                    return key

        return "key doesn't exist"

    def export_dy_communities(self, base_dir):
        utilities.write_json(os.path.join(base_dir, "DY_COMM_10.json"), self.DY_COMMS)



def main():
    base_dir = "/home/c6/Desktop/OpenWPM/jsons/community_tracking/real_graphs"
    # bootstrapping
    comm_track_obj = DynamicCommunityTracking()
    initial_snap_dir = base_dir + "/2010"
    initial_snap_comms = utilities.get_files_in_a_directory(initial_snap_dir)
    comm_track_obj.bootstrap(initial_snap_comms)

    # community_tracking
    years = np.arange(2011, 2020, 1)
    for year in years:
        print(year)
        communities = utilities.get_files_in_a_directory(os.path.join(base_dir, str(year)))
        comm_track_obj.one_to_one_match(communities, base_dir)
        comm_track_obj.update_front(year)
        #comm_track_obj.process_death(year)

    comm_track_obj.export_dy_communities(base_dir)


if __name__ == '__main__':
    main()
