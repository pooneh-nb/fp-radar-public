import pandas as pd
from myCodes.AST import utilities
import jsons
import os


def create_non_fp_dataframe(path_to_non_fp, path_non_fp_dataframe):

    non_fp_files = utilities.get_files_in_a_directory(path_to_non_fp)
    # create df file
    df_non_fp = pd.DataFrame(columns=['url_id', 'is_backup', 'hash_script', 'date_snapshot'])

    for file_name in non_fp_files:
        if file_name.split('/')[-1].split('|')[0] == 'yes':
            url_id = file_name.split('/')[-1].split('|')[-1]
            hash_script = file_name.split('/')[-1].split('|')[1]
            date_snapshot = file_name.split('/')[-1].split('|')[2]
            year = file_name.split('/')[-1].split('|')[2][0:4]
            df_non_fp = df_non_fp.append({'url_id': url_id, 'is_backup': "has_snapshot", 'hash_script': hash_script,
                              'date_snapshot': date_snapshot, 'year': year}, ignore_index=True)
        else:
            url_id = file_name.split('/')[-1].split('|')[-1]
            df_non_fp = df_non_fp.append({'url_id': url_id, 'is_backup': "No_snapshot", 'hash_script': "",
                              'date_snapshot': "", 'year': ""}, ignore_index=True)

    df_non_fp.to_csv(os.path.join(path_non_fp_dataframe, "non_fp_df.csv"), index=False, header=True)
    df_non_fp.to_pickle(os.path.join(path_non_fp_dataframe, "non_fp_df.pkl"), protocol=3)


def create_fp_dataframe(path_to_fp, path_fp_dataframe):

    fp_files = utilities.get_files_in_a_directory(path_to_fp)
    # create df file
    df_fp = pd.DataFrame(columns=['url_id', 'is_backup', 'hash_script', 'date_snapshot', 'year'])
    for file_name in fp_files:
        if file_name.split('/')[-1].split('|')[0] == 'yes':
            url_id = file_name.split('/')[-1].split('|')[-1]
            hash_script = file_name.split('/')[-1].split('|')[1]
            date_snapshot = file_name.split('/')[-1].split('|')[2]
            year = file_name.split('/')[-1].split('|')[2][0:4]
            df_fp = df_fp.append({'url_id': url_id, 'is_backup': "has_snapshot", 'hash_script': hash_script,
                              'date_snapshot': date_snapshot, 'year': year}, ignore_index=True)
        else:
            url_id = file_name.split('/')[-1].split('|')[-1]
            df_fp = df_fp.append({'url_id': url_id, 'is_backup': "No_snapshot", 'hash_script': "",
                              'date_snapshot': "", 'year': ""}, ignore_index=True)

    df_fp.to_csv(os.path.join(path_fp_dataframe, "fp_df.csv"), index=False, header=True)
    df_fp.to_pickle(os.path.join(path_fp_dataframe, "fp_df.pkl"), protocol=3)


def main():
    path_to_non_fp = "/home/pooneh/Desktop/OpenWPM/jsons/main_dataset/non_fp_scripts"
    path_non_fp_dataframe = "/home/pooneh/Desktop/OpenWPM/jsons/dataframes"
    create_non_fp_dataframe(path_to_non_fp, path_non_fp_dataframe)

    #path_to_fp = "/home/c6/Desktop/OpenWPM/jsons/main_dataset/fp_scripts"
    #path_fp_dataframe = "/home/pooneh/Desktop/OpenWPM/jsons/dataframes"
    #create_fp_dataframe(path_to_fp, path_fp_dataframe)


if __name__ == '__main__':
    main()

