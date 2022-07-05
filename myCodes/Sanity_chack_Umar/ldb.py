import os
import plyvel
import json
from myCodes.AST import utilities
import shutil


def html_creator():
    packed_files_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/packed_files"
    packed_html_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/unpacking/packed_html_files"

    packed_files = utilities.get_files_in_a_directory(packed_files_dir)

    for script in packed_files:
        file_name = script.split('/')[-1]
        print(file_name)
        if os.stat(script).st_size != 0:
            script_text = utilities.read_dill_compressed(script)
            try:
                if '<!DOCTYPE html>' in script_text:
                    html_files = os.path.join(packed_html_dir, file_name + '.html')
                    utilities.write_content(html_files, script_text)
                else:
                    utilities.write_content(os.path.join(packed_html_dir + '/js/', file_name + '.js'),
                                            script_text)
                    js_file = "http://0.0.0.0:8000/js/" + file_name + '.js'
                    html_text = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>Title</title>
                        </head>
                        <body>
                        <script src='""" + js_file + """'></script>
                        </body>
                        </html>"""
                    html_files = os.path.join(packed_html_dir, file_name + '.html')
                    utilities.write_content(html_files, html_text)
            except Exception as ex:
                # print("text", script_text)
                print("Exception", ex)
        else:
            print("text empty")


def download_packed_files(ldb):
    # in this function we separate packed and non_packed files using their hash name
    all_files_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/all_files"
    packed_files_dir = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/packed_files"

    packed_hash_list = set(utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/packed_hash_list.json"))
    all_files = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/jsfiles_hash.json")

    for hash in all_files:
        script_text = ldb.get(bytes(hash, 'utf-8')).decode()
        if hash in packed_hash_list:
            utilities.write_dill_compressed(os.path.join(packed_files_dir, hash), script_text)
        else:
            utilities.write_dill_compressed(os.path.join(all_files_dir, hash), script_text)


def extract_all_ldb_keys(ldb):
    # save all the js hashes as the keys of files

    all_keys = []
    for db_key, db_value in ldb:
        all_keys.append(db_key.decode())
        print(db_key.decode())
    print(len(all_keys))
    with open('/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/jsfiles_hash.json', 'w') as keys:
        json.dump(all_keys, keys, indent=3)


def download_jsfiles(ldb):

    with open('/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/jsfiles_hash.json', 'rt') as u:
        url_hash = json.load(u)
    packed_hash = "/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/packed_hash"
    packed_hash_list = []
    for script_hash in url_hash:
        script_text = ldb.get(bytes(script_hash, 'utf-8')).decode()
        if "eval(" in script_text or "Function(" in script_text:
            packed_hash_list.append(script_hash)
    utilities.write_json('/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/packed_hash_list.json',packed_hash_list)
            #utilities.write_dill_compressed(os.path.join(packed_hash, script_hash), script_text)


def main():
    base_directory = '/home/c6/Desktop'
    # Connect to content database
    #ldb = plyvel.DB(os.path.join(base_directory, 'content.ldb'))
    #extract_all_ldb_keys(ldb)
    #download_jsfiles(ldb)
    #download_packed_files(ldb)
    #pack = utilities.read_json('/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/packed_hash_list.json')
    #print(len(pack))
    html_creator()


if __name__ == '__main__':
    main()