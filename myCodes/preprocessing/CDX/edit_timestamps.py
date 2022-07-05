import jsons
from myCodes.AST import utilities


def edit_times():
    existing_non_fp = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots.json")

    for key_url_id, value in existing_non_fp.items():
        idx_date = 0
        for timestamp in value['snapshots']:
            if int(timestamp[0:4]) < 2010:
                value['snapshots'].remove(timestamp)
                value['digest'].pop(idx_date)
            idx_date += 1

    utilities.write_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots2.json", existing_non_fp)


def number_of_snapshots():
    non_df = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/CDX_api/dataframe/existing_fp_snapshots2.json")
    apr = 0
    for url_id, value in non_df.items():
        apr = apr + len(value['snapshots'])
    print(apr)


edit_times()
number_of_snapshots()