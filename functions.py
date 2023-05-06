# use snake case names
# functions
# getFileNamesInDir
# file_renamer: file_path, new_name
# file_name_purifier: file_name, chars_to_remove_from_file_name
# directory_purifier: directory_name, chars_to_remove_fromfile_names

import os

def directory_purifier(directory_name, chars_to_remove_from_file_names, dry_run= True):

    files = os.listdir(directory_name)
    files_renamed = []

    for file_name in files:
        new_file_name = file_name_purifier(file_name, chars_to_remove_from_file_names)
        if new_file_name != file_name:
            print("new file name: ", new_file_name, "old file name: ", file_name)
            files_renamed.append((file_name, new_file_name))
            file_path = os.path.join(directory_name, file_name)
            if not dry_run:
                rename_file(file_path, new_file_name)
                print(f"Renamed file {file_name} to {new_file_name} (dry run)")

    return files_renamed


def directory_files_renamed_sequentially_by_last_edit(directory_path, ascending=False, dry_run = True):

    files_sorted_by_last_edit = directory_files_sorted_by_newest_edit(directory_path)
    new_old_file_names = add_no_to_sorted_file_names(files_sorted_by_last_edit, ascending=ascending)
    if dry_run:
        return new_old_file_names
    rename_directory_files(directory_path, new_old_file_names)

    

def rename_file(file_path, new_name):
    os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))

def file_name_purifier(file_name, chars_to_remove_from_file_name):
    file_name = file_name.replace(chars_to_remove_from_file_name, '')
    return file_name


def directory_files_sorted_by_newest_edit(directory_path):
    "sorted by oldest edit first"
    directory_list = os.listdir(directory_path)

    sorted_directory_list = sorted(directory_list, 
                                   key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))

    return sorted_directory_list

def add_no_to_sorted_file_names(file_names_sorted_in_descending, ascending=False):
    
    if not ascending: # descending
        file_names_sorted_in_descending.reverse()

    numbered_file_names = [(name, f"{i+1}_{name}") for i, name in enumerate(file_names_sorted_in_descending)]

    return numbered_file_names

def rename_directory_files(directory_path, old_new_file_names):
    for old_file_name, new_file_name in old_new_file_names:
        rename_file(os.path.join(directory_path, old_file_name), new_file_name)


def main():
    # tmpdir = ~/tmp
    tmpdir = os.path.expanduser("~/tmp")
    print(directory_files_renamed_sequentially_by_last_edit(tmpdir, ascending=True, dry_run=True))

if  __name__ == "__main__":
    main()
