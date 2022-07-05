import os
import json
from myCodes.AST import utilities
import requests
import time

def js_snapshot_downloader(source_directory_addr, js_files_addr):

    all_files = utilities.get_files_in_a_directory(source_directory_addr)

    for file_name in all_files:
        if file_name.split('/')[-1].split('|')[0] == 'yes':
            compressed_file = utilities.read_dill_compressed(file_name)
            print(type(compressed_file))
            utilities.write_dill(os.path.join(unzip_directory, file_name.split('/')[-1]), compressed_file)


source_directory_addr = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/test_ast"
unzip_directory = "/home/pooneh/Desktop/OpenWPM/jsons/downloaded_files/non_fp_javascripts/unzip"
js_snapshot_downloader(source_directory_addr, unzip_directory)


