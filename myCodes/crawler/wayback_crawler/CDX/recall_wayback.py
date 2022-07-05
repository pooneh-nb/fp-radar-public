import os.path
from datetime import date, timedelta
import time
import requests
import json
import os
from multiprocessing import Pool as ThreadPool
import multiprocessing
import itertools
import myCodes.AST.utilities as utilities

manager = multiprocessing.Manager()
remaining_unprocessed_files = manager.list()
processed_files = []

all_files_path = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots.json"
with open(all_files_path ) as p:
    unprocessed_script_url_list = json.load(p)

# input: url_id and url script in encoded format. and the path to download json files
# output: for each url, if CDX API has any snapshot, it will return a json file in response
def recall_wayback(id_time_script_url, gathered_files_path):

    encoded_url = id_time_script_url.split('|')[2]
    url_id = id_time_script_url.split('|')[0]
    requested_time = id_time_script_url.split('|')[1]
    digest = id_time_script_url.split('|')[-1]


    try:
        has_response = 0
        response = requests.get("http://web.archive.org/web/" + requested_time + "0000" + "/" + encoded_url)
        has_response = 1
        if response.status_code == 400:
            utilities.append_file('/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/fp/wayback_crawl_err_logs.json',
                                    str(url_id) + "|" + str(requested_time) + "|" + str(response.status_code))
        if not response.ok:
            print(str(requested_time) + " : " + str(response.status_code))
            time_to_sleep = int(response.headers["Retry-After"])
            if time_to_sleep:
                time.sleep(int(response.headers["Retry-After"]))
            else:
                time.sleep(15)
        if response.status_code == 200:
            js_content = response.text
            if js_content != "":
                utilities.write_dill_compressed(
                    os.path.join(gathered_files_path, "yes|" + digest + "|" + requested_time + "|" + url_id),
                    js_content)
                print(url_id + " has a snapshot at " + requested_time)
                # if requested_time[0:6] != response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                # print(requested_time,  response_json['archived_snapshots']['closest']['timestamp'], url_id)
            else:
                print(url_id, requested_time, " doesn't have snapshot")
                utilities.append_file(
                    '/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/fp/no_response_fp.json',
                    url_id + "|" + requested_time)
                # completeness = False

    except Exception as inst:
        if has_response == 0:
            print("OOps: !", inst, url_id)
            utilities.append_file(
                '/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/fp/wayback_crawl_err_logs.json',
                                    str(url_id) + "|" + str(requested_time) + "|" + str(inst))
        if has_response == 1:
            print("OOps: !", inst, url_id)
            utilities.append_file(
                '/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/fp/wayback_crawl_err_logs.json',
                str(url_id) + "|" + str(requested_time) + "|" + str(inst) + "|" + str(response.status_code))
        time.sleep(15)
        # completeness = False
        pass


def remaining_checker(url_time):
    if url_time not in processed_files:
        time_index = unprocessed_script_url_list[url_time.split('|')[0]]['snapshots'].index(
            url_time.split('|')[1])
        script_url = unprocessed_script_url_list[url_time.split('|')[0]]['encoded_url']
        digest = unprocessed_script_url_list[url_time.split('|')[0]]['digest'][time_index]
        remaining_unprocessed_files.append(url_time + "|" + script_url + "|" + digest)
        print(len(remaining_unprocessed_files))


def create_queued_files(gathered_files_path):
    print("create")
    #remaining_unprocessed_files = []
    all_unprocessed_files = []

    # collect processed_files: url_ID|snapshot
    gathered_files = utilities.get_files_in_a_directory(gathered_files_path)
    for fil in gathered_files:
        processed_files.append(fil.split('/')[-1].split('|')[-1] + "|" + fil.split('/')[-1].split('|')[2])
    print("processed: ", len(processed_files))
    # collect ALl url_snapshots
    for url_id_key, val in unprocessed_script_url_list.items():
        for timestamp in val['snapshots']:
            all_unprocessed_files.append(url_id_key+"|"+timestamp)
    print("all: ", len(all_unprocessed_files))

    ## local processor
    local_cpu_to_relax = 0
    pool_local = ThreadPool(processes=multiprocessing.cpu_count() - local_cpu_to_relax)
    results = pool_local.map(remaining_checker, all_unprocessed_files)
    pool_local.close()
    pool_local.join()

    """for url_time in all_unprocessed_files:
        if url_time not in processed_files:
            time_index = unprocessed_non_fp_script_url_list[url_time.split('|')[0]]['snapshots'].index(url_time.split('|')[1])
            script_url = unprocessed_non_fp_script_url_list[url_time.split('|')[0]]['encoded_url']
            digest = unprocessed_non_fp_script_url_list[url_time.split('|')[0]]['digest'][time_index]
            remaining_unprocessed_files.append(url_time+"|"+script_url+"|"+digest)
            print(len(remaining_unprocessed_files))"""

    print("remaining: ", len(list(remaining_unprocessed_files)))

    cpu_to_relax = 10
    #pool = ThreadPool(processes=1)
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.starmap(recall_wayback,
                           zip(list(remaining_unprocessed_files), itertools.repeat(gathered_files_path)))
    pool.close()
    pool.join()


def main():
    # collect for non_FP urls
    """gathered_files = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_js"
    all_files_path = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_snapshots.json"
    with open(all_files_path ) as p:
        unprocessed_non_fp_script_url_list = json.load(p)
    #selected_dictionary = dict(list(unprocessed_non_fp_script_url_list.items())[9001:10000])
    json_write_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_js"
    create_non_fp_queued_files(unprocessed_non_fp_script_url_list, gathered_files)"""

    #collect for FP urls
    gathered_files = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_javascripts"
    all_files_path = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots.json"
    with open(all_files_path) as p:
        unprocessed_fp_script_url_list = json.load(p)
    # selected_dictionary = dict(list(unprocessed_non_fp_script_url_list.items())[9001:10000])
    #json_write_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_javascripts"
    create_queued_files(gathered_files)

if __name__ == '__main__':
    main()


