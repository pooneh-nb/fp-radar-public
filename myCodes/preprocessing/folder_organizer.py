import os, shutil
from myCodes.AST import utilities
from shutil import copy


# return subfolder names inside a folder
def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


# create a folder based on url_id
def file_based_on_url_id_organizer(source, destination):
    all_files = utilities.get_files_in_a_directory(source)
    for file_name in all_files:
        folder = os.path.join(destination,
                              file_name.split('/')[-1].split('|')[-1])
        if not os.path.exists(folder):
            os.makedirs(folder)
        copy(file_name, folder)


# create a folder based on date
def file_based_on_date_organizer(source, destination):
    all_files = utilities.get_files_in_a_directory(source)

    for file_name in all_files:
        if file_name.split('/')[-1].split('|')[0] == 'yes':
            file_date = file_name.split('/')[-1].split('|')[-2][0:4]
            copy(file_name, os.path.join(destination, file_date))



def copy_files_to_main_dir():
    dest = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_js"
    source_folder = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/c6_non_fp_javascripts"
    all_files = utilities.get_files_in_a_directory(source_folder)
    for file_n in all_files:
        copy(file_n, dest)


# collect all non-fp js files in one directory: jsons/main_dataset/non_fp_scripts
def main_non_fp_directory():
    source_of_separated_folders = "/home/pooneh/Documents/dockdockgo/non_FP_files"
    dest = '/home/c6/sktop/OpenWPM/jsons/main_dataset/non_fp_scripts'
    list_of_non_fp_folders = fast_scandir(source_of_separated_folders)
    for folder in list_of_non_fp_folders:
        file_name = utilities.get_files_in_a_directory(folder)
        for js_file in file_name:
            copy(js_file, dest)

def main():

    #source_directory_path = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/9000-10000"
    #all_files = utilities.get_files_in_a_directory(source_directory_path)
    #file_based_on_date_organizer(all_files)
    #copy_files_to_main_dir()
    #main_non_fp_directory()

    source_of_non_fp_files = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_js"
    dest_of_non_fp_date_organized = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_date_organized"
    file_based_on_date_organizer(source_of_non_fp_files, dest_of_non_fp_date_organized)


if __name__ == '__main__':
    main()

