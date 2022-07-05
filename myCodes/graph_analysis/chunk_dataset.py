from myCodes.AST import utilities
from shutil import copy

script_directory = "/home/pooneh/Desktop/OpenWPM/jsons/main_dataset/non_fp_date_organized/2019"
script_list = utilities.get_files_in_a_directory(script_directory)

c_script = "/home/pooneh/Desktop/OpenWPM/jsons/AST/wayback_results/2019/partitioned_dataset/c6"

for script in script_list[210000:]:
    copy(script, c_script)
