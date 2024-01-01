'''
Run this script in the directory in which you want to 
delete files form a perticular extension.
Pass args for extensions to delete without '-'
'''


import os
import sys

exts = sys.argv

pwd = os.getcwd()
all_files = 0
del_files = 0
del_file_names = []

if len(exts) > 1:
    print(f'Deleting all files with extension: {exts}')
    for path, subdirs, files in os.walk(pwd):
        for name in files:
            all_files += 1
            if name.split('.')[-1] in exts:
                del_files += 1
                file_name = os.path.join(path, name)
                del_file_names.append(file_name)
else:
    print("No specifications for deletions")

if len(del_file_names) > 1:
    permission = input("Are you sure delete {} files out of {}? ".format(del_files, all_files))
    if permission.lower() in ['yes', 'y', '']:
        for file in del_file_names:
            os.remove(file)
            print("Deleted: {}".format(file))
        print("Deleted all files")
    else:
        print("Delete aborted")
