# in this code, we extract unique snapshots for each url
from myCodes.AST import utilities
import urllib.parse as url
import multiprocessing
from multiprocessing import Pool as Threadpool
import os
import pandas as pd


manager = multiprocessing.Manager()
url_snapshot = manager.dict()


def existing_snapshots(json_file):
    try:
        log_snapshot = set()
        log_digest = set()
        snapshot = []
        digest = []
        if json_file.split('/')[-1].split('|')[0] == 'yes':
            url_id = json_file.split('/')[-1].split('|')[1].split('.')[0]
            non_json = utilities.read_json(json_file)
            for line in non_json[1:]:
                if line[3] == "200":
                    print("200")
                    if line[4] not in log_digest:
                        print("new digest")
                        if line[1][0:6] not in log_snapshot:
                            print("new snapshot")
                            log_snapshot.add(line[1][0:6])
                            log_digest.add(line[4])
                            snapshot.append(line[1][0:8])
                            print(snapshot)
                            digest.append(line[4])
                            print(digest)
            url_snapshot[url_id] = {'snapshots': snapshot,
                                    'origin': line[0],
                                    'encoded_url': url.quote(line[0]),
                                    'digest': digest}
    except Exception as inst:
        print(url_id, inst)
        pass

def edit_empty_snapshots():
    existing_non_fp = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots.json")
    for url_id_key, value in existing_non_fp.items():
        if len(value['snapshots']) == 0:
            cdx_json = utilities.read_json(os.path.join
                                           ("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/non_fp_jsons",
                                            "yes|"+url_id_key+".json"))
            for line in cdx_json[1:]:
                if line[3] == "-":
                    existing_non_fp[url_id_key]['snapshots'].append(line[1][0:8])
                    break
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots2.json", existing_non_fp)


def edit_empty_digest():
    existing_non_fp = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots.json")
    for url_id_key, value in existing_non_fp.items():
        if len(value['digest']) == 0:
            cdx_json = utilities.read_json(os.path.join
                                           ("/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/non_fp_jsons",
                                            "yes|" + url_id_key + ".json"))
            for line in cdx_json[1:]:
                if line[1][0:8] == value['snapshots'][0]:
                    print(1)
                    existing_non_fp[url_id_key]['digest'].append(line[4])
                    break
    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots2.json",
                         existing_non_fp)


def extract_full_snapshots(json_file):
        log_snapshot = set()
        snapshot = []
        year = set()
        if json_file.split('/')[-1].split('|')[0] == 'yes':
            url_id = json_file.split('/')[-1].split('|')[1].split('.')[0]
            non_json = utilities.read_json(json_file)
            for line in non_json[1:]:
                if int(line[1][0:4]) > 2009:
                    if line[1][0:6] not in log_snapshot:
                        log_snapshot.add(line[1][0:6])
                        snapshot.append(line[1][0:6])
                        year.add(line[1][0:4])

            url_snapshot[url_id] = {'snapshots': snapshot, 'year': list(year), 'origin': line[0]}
        print(len(url_snapshot))

def main():
    cpu_to_relax = 1
    # calling extract_full_snapshots
    non_fp_dir = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/CDX_jsons/fp_jsons"
    non_fp_jsons = utilities.get_files_in_a_directory(non_fp_dir)
    non_fp_json_files = []
    for non_fp_json in non_fp_jsons:
        non_fp_json_files.append(non_fp_json)

    pool = Threadpool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    #pool = Threadpool(processes=1)
    results = pool.map(extract_full_snapshots, non_fp_json_files)
    print("multiprocessing done")
    path_to_write_non_fp = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_full_snapshots.json"
    utilities.write_json(path_to_write_non_fp, dict(url_snapshot))
    print("save file")

    # calling existing_non_fp_snapshots()
    """non_fp_dir = "/home/pooneh/Desktop/OpenWPM/jsons/CDX_api/non_fp_jsons"
    non_fp_jsons = utilities.get_files_in_a_directory(non_fp_dir)
    non_fp_json_files = []
    for non_fp_json in non_fp_jsons:
        non_fp_json_files.append(non_fp_json)

    #pool = Threadpool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    pool = Threadpool(processes=1)
    results = pool.map(existing_snapshots, non_fp_json_files)
    print("multiprocessing done")
    path_to_write_non_fp = "/home/pooneh/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots.json"
    utilities.write_json(path_to_write_non_fp, dict(url_snapshot))
    print("save file")"""


    """
    # calling existing_fp_snapshots
    fp_dir = "/home/pooneh/Desktop/OpenWPM/jsons/CDX_api/fp_jsons"
    fp_jsons = utilities.get_files_in_a_directory(fp_dir)
    fp_json_files = []
    for fp_json in fp_jsons:
        fp_json_files.append(fp_json)

    pool = Threadpool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.map(existing_snapshots, fp_json_files)
    print("multiprocessing done")
    path_to_write_fp = "/home/pooneh/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots.json"
    utilities.write_json(path_to_write_fp, dict(url_snapshot))
    print("save file")"""


#if __name__ == '__main__':
    #main()
url_snaps = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_full_snapshots.json")

num_snaps_df = pd.DataFrame(columns=['url_id', 'num_snapshots'])
for url_id, value in url_snaps.items():
    num_snaps_df =  num_snaps_df.add([url_id, len(value['snapshots'])])



