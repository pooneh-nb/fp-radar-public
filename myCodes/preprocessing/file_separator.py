import itertools

from myCodes.AST import utilities
from shutil import move
import os
import multiprocessing
from multiprocessing import Pool as ThreadPool


def zip_files(script, Destination):
        new_name = script.replace('.html', '').split('/')[-1]
        read_file = utilities.read_file(script)
        utilities.write_dill_compressed(os.path.join(Destination, new_name), read_file)


def move_files():
    large_file_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized/" \
                           "2020/test"
    large_file = utilities.get_files_in_a_directory(large_file_directory)
    destination = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized/" \
                  "2020/all"

    for script in large_file:
        new_name = script.split('/')[-1]
        move(script, os.path.join(destination, new_name))


def main():
    large_file_directory = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized/" \
                           "2020/unpacked_scripts"
    large_file = utilities.get_files_in_a_directory(large_file_directory)
    Destination = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized/" \
                  "2020/test"

    cpu_to_relax = 3
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    pool.starmap(zip_files, zip(large_file, itertools.repeat(Destination)))

main()
move_files()


