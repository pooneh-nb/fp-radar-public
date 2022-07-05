from myCodes.AST import utilities
import os
import Levenshtein as lv
import multiprocessing
from multiprocessing import Pool as ThreadPool
import json

manager = multiprocessing.Manager()
hash_report = manager.list()


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def unify_hash_files(url_id):
    print(url_id.split('/')[-1])
    hash_files = utilities.get_files_in_a_directory(url_id)
    num_original_files = len(hash_files)
    # print(str(len(hash_files)) + url_id)
    for js_file in hash_files:
        if js_file.split('/')[-1].split('|')[0] == 'no':
            print("no back up")
            hash_report[url_id] = {'num_original_files': 0, 'num_after_unifying': 0, 'isbackup': False}
            break
        for js_file2 in hash_files:
            a = js_file.split('/')[-1].split('|')[1]
            b = js_file2.split('/')[-1].split('|')[1]
            if js_file.split('/')[-1].split('|')[1] == js_file2.split('/')[-1].split('|')[1]:
                continue
            else:
                difference_hash = lv.distance(utilities.read_dill_compressed(js_file), utilities.read_dill_compressed(js_file2))
                print(difference_hash)
                if lv.distance(utilities.read_dill_compressed(js_file), utilities.read_dill_compressed(js_file2)) < 50:
                    os.remove(js_file2)
    num_after_unifying = utilities.get_files_in_a_directory(url_id)
    hash_report[url_id] = {'num_original_files': num_original_files, 'num_after_unifying': num_after_unifying, 'isbackup': True}



def main():
    js_addr = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/date_organizer"
    list_of_date_organized_urls = fast_scandir(js_addr)
    num_cpu_workers = 5
    pool = ThreadPool(processes=num_cpu_workers)
    results = pool.map(unify_hash_files, list_of_date_organized_urls)
    with open("/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/hash_report.json", 'w') as f:
        json.dump(hash_report, f, sort_keys=True, indent=4)
    pool.close()
    pool.join()
    # unify_hash_files(list_of_date_organized_urls)

    # a = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/date_organizer/9304/yes|0b41b953e1bfeb561fc409c35b239124|20150428|9304"
    # b = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/date_organizer/9304/yes|0c4c382be647baeb5d692970a25d80f9|20180612|9304"
    # print(lv.distance(a,b))


if __name__ == '__main__':
    main()
