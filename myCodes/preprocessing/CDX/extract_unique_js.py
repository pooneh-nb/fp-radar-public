from myCodes.AST import utilities
import shutil
import os



all_js_files = utilities.get_files_in_a_directory("/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_date_organized/2010")
unique_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/non_fp_date_organized/2010_unique"
if not os.path.exists(unique_directory):
    os.makedirs(unique_directory)
unique_hash = set()
for fil in all_js_files:
    script_hash = fil.split('/')[-1].split('|')[1]
    if script_hash not in unique_hash:
        unique_hash.add(script_hash)
        shutil.copy(fil, unique_directory)
