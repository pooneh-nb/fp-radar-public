import json
from datetime import date, timedelta
from multiprocessing import Pool as ThreadPool
from multiprocessing import current_process, get_logger, log_to_stderr
import logging
import multiprocessing
import time
import requests
import urllib3
import urllib as u
import os
from myCodes.AST import utilities
import itertools
import hashlib as hash



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
err_logs = {'errors': []}


def availability_api(id_script_url, downloaded_file_dir):
    script_url = id_script_url.split('|')[-1]
    url_id = id_script_url.split('|')[0]
    noBackground = True
    start_date = date(2010, 1, 1)
    end_date = date(2020, 12, 1)
    delta = timedelta(days=30)
    #print("requested url: " + script_url)
    start = time.time()
    print("Processing: " + script_url + " by " + current_process().name)
    while start_date <= end_date:
        hashed_list = []
        #print("while " + current_process().name)
        try:
            requested_time = start_date.strftime("%Y%m%d")
            #print(requested_time+ " for" + script_url)
            proxies = {'https': 'http://91.205.174.26'}
            response = requests.get(
                "https://archive.org/wayback/available?url=" + script_url + "&timestamp=" + requested_time
                , verify=False)
            if not response.ok:
                print(str(requested_time) + " : " + str(response.status_code) + ": "+ current_process().name)
                time.sleep(int(response.headers["Retry-After"]))
                #print("wait for " + script_url + " by " + current_process().name)
                continue
            if response.status_code == 200:
                #print(str(response.status_code) + " " + current_process().name)
                response_json = response.json()
                if response_json['archived_snapshots'] != {}:
                    if requested_time[0:6] == response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                        hash_script = hash.md5(response.content).hexdigest()
                        fp_js_directory_list_files = utilities.get_files_in_a_directory(downloaded_file_dir)
                        for hash_name in fp_js_directory_list_files:
                            hashed_list.append(hash_name.split('/')[-1].split('|')[1])
                        #print(hash_script + current_process().name)
                        #time.sleep(1)
                        if hash_script not in hashed_list:
                            closest_date = response_json['archived_snapshots']['closest']['timestamp'][0:8]
                            url = response_json['archived_snapshots']['closest']['url'][42:]
                            noBackground = False
                        utilities.write_dill_compressed(
                            os.path.join(downloaded_file_dir, "yes|"+hash_script+"|"+closest_date+"|"+url_id), response.content)
                        print(script_url + " has a snapshot at " + closest_date)

        except Exception as inst:
            print("OOps: !", inst)
            utilities.append_file('/jsons/error/err_logs.json', script_url + ' Failed at '
                                  + str(requested_time) + " error: " + str(inst) + "\n")
            time.sleep(15)
            pass
        start_date += delta

    if noBackground:
        print(script_url + " doesn't have any background")
        utilities.write_dill_compressed(
            os.path.join(downloaded_file_dir, "no|" + url_id), "")
    end = time.time()

    print(script_url + " is done in:")
    print(end-start)


def create_fp_queued_files(unprocessed_fp_script_url_list, js_write_directory, cpu_to_relax):

    remaining_unprocessed_fp_script_url = []
    #remaining_unprocessed_fp_script_url = {}
    all_unprocessed_fp_script_url_list = unprocessed_fp_script_url_list  # dict hash: url, url_ID
    processed_fp_script_directory = utilities.get_files_in_a_directory(js_write_directory)
    processed_fp_script_url_list = []
    for a in processed_fp_script_directory:
        #b= a.split('/')[-1].split('|')[-1]
        #url = b.replace('_', "/")
        processed_fp_script_url_list.append(a.split('/')[-1].split('|')[-1])

    for unprocessed_key, unprocessed_value in all_unprocessed_fp_script_url_list.items():
        if str(unprocessed_value['url_id']) not in processed_fp_script_url_list:
            remaining_unprocessed_fp_script_url.append(str(unprocessed_value['url_id']) + "|" + unprocessed_value['url'])
            #remaining_unprocessed_fp_script_url.append(unprocessed_value['url_id'] + + unprocessed_value['url'])


    print(len(remaining_unprocessed_fp_script_url))
    # IO bound jobs -> multiprocessing.pool.ThreadPool
    # CPU bound jobs -> multiprocessing.Pool
    #num_cpu_workers = multiprocessing.cpu_count() - cpu_to_relax
    num_cpu_workers = 5
    pool = ThreadPool(processes=num_cpu_workers)
    #for w in pool._pool:
        #w.name = w.name.replace('ForkPoolWorker', 'Worker')
    #print([w.name for w in pool._pool])
    # ['ThreadPoolWorker-1', 'ThreadPoolWorker-2', 'ThreadPoolWorker-3', 'ThreadPoolWorker-4']
    #multiprocessing.log_to_stderr()
    #logger = multiprocessing.get_logger()
    #logger.setLevel(logging.INFO)
    #print(logger)
    #pool.daemon = False
    results = pool.starmap(availability_api, zip(remaining_unprocessed_fp_script_url, itertools.repeat(js_write_directory)))
    pool.close()
    pool.join()


def main():
    #unprocessed_fp_script_url_list = []
    #with open("/home/pooneh/Desktop/OpenWPM/jsons/third_parties/fp_3rd_url_20k.json") as p:
        #unprocessed_fp_script_url_list = json.load(p)
    with open("/jsons/third_parties/fp_3rd_url_20k.json") as p:
        unprocessed_fp_script_url_list = json.load(p)
    js_write_directory = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/fp_javascripts"
    cpu_to_relax = 3
    create_fp_queued_files(unprocessed_fp_script_url_list, js_write_directory, cpu_to_relax)


if __name__ == '__main__':
    main()