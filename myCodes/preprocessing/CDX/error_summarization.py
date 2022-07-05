import pandas as pd
import os
import csv
from myCodes.AST import utilities


def extract_df():
    with open("/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/non_fp/wayback_crawl_err_logs.json") as ff:
        error_log = ff.read().splitlines()
    path_df = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/non_fp/dataframes"
    err_df = pd.DataFrame(columns={'url_id', 'timestamp', 'error_type'})
    for err in error_log:
        if int(err.split('|')[1][0:4]) > 2009:
            url_id = err.split('|')[0]
            timestamp = err.split('|')[1]
            error_type = err.split('|')[-1]
            err_df = err_df.append({'url_id': url_id, 'timestamp': timestamp, 'error_type': error_type}, ignore_index=True)
            err_df.to_csv(os.path.join(path_df, "non_fp_err_log.csv"), index=False, header=True)


def data_error_summary():

    error_df = pd.read_csv("/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/error/non_fp/dataframes/non_fp_err_log.csv")
    a_df = error_df.groupby(['error_type']).size().reset_index()
    sort_df = error_df.sort_values(['url_id']).reset_index()
    adfter_sort = sort_df[sort_df['error_type'] == "403"]
    adfter_after = adfter_sort[adfter_sort['url_id'] == 429]
    #after = a_df[a_df['error_type'] == "403"]

    print(adfter_after)


def timeaverage():
    url_snaps_fp = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_full_snapshots.json")
    url_snaps_non_fp = utilities.read_json(
        "/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_non_fp_full_snapshots.json")
    length_non_fp_URls = len(url_snaps_non_fp.keys())
    length_fp_URls = len(url_snaps_fp.keys())

    non_fp_snapshots = 0
    non_fp_time_duration =0
    for url_id, value in url_snaps_non_fp.items():
        non_fp_snapshots = non_fp_snapshots + len(value['snapshots'])
        year_list = list(map(int, value['year']))
        duration = max(year_list)-min(year_list)
        if duration == 0:
            duration = 1
        if duration < 0:
            print("eeeeee")
        non_fp_time_duration = non_fp_time_duration + duration
    print(non_fp_time_duration)

    fp_snapshots = 0
    fp_time_duration = 0
    for url_id, value in url_snaps_fp.items():
        non_fp_snapshots = non_fp_snapshots + len(value['snapshots'])
        year_list = list(map(int, value['year']))
        duration = max(year_list) - min(year_list)
        if duration == 0:
            duration = 1
        if duration < 0:
            print("eeeeee")
        fp_time_duration = fp_time_duration + duration
    print(fp_time_duration)

    average_num_snapshot = (non_fp_snapshots + fp_snapshots) / (length_non_fp_URls + length_fp_URls)
    average_duration = (non_fp_time_duration + fp_time_duration) / (length_non_fp_URls + length_fp_URls)
    print(average_num_snapshot)
    print(average_duration)



#extract_df()
#data_error_summary()
timeaverage()