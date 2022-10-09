# fileSystemComparison.py
# Paige Mortensen
# CS 446 PA3 - compare and contrast single level file directories with hierarchical file directories

    # QUESTION 1: discuss any similarities/dissimilarities in the printed output between singleLevelFiles.txt and
    # hierarchicalFiles.txt explain the reason these differences or similarities exist
# For the similarities within the two files, all the generated text files have the same size of 0 bytes and are listed
# in the file. But, for the differences, the size and presence of the directories and the access order of each file is
# different. The directories have an average size of 4096 bytes because they each contain 10 files, whereas the
# single-level directory does not contain any subdirectories (and therefore no subdirectories are listed). As for the
# access process, in the single level directory, all 100 files are randomly accessed and therefore listed out-of-order
# in terms of their numbering. But, in the hierarchical level system, the directories are randomly gatered and printed,
# but so are the files within them. To explain, the system grabbed a directory and then grabbed all 10 files. Then the
# next directory is accessed and the next ten files are listed. This means that not all 100 files are intermingled, but
# that each set of 10 files is. This is because of how we have our files nested inside our folders and how they are
# being traversed.

    # QUESTION 2: We have a simple file system that only supports a single-level architecture. Files can have
    # arbitrarily long names and the root directory can have an arbitrary number of files. How could we implement
    # something similar to a hierarchical file system? (hint, think about approximating a path)
# In this file system, we the user could devise a naming pattern for the files. For example, if we wanted to place
# something in an arbitrary "directory", we could name our files something like dir1_filename_1.txt, dir1_filename_2.txt
# Then for the second "directory", we could name our files dir2_filename_1.txt, dir2_filename_2.txt. This would
# automatically sort the files in alphabetical/numerical order (making the assumption that the system does this like
# normal), and would allow the user to easier search for and find their files based on name alone. Their files wouldn't
# be in nested folders and would still be in one long list, but at least they could have some way of creating a "path"
# and or "nesting" their folders with a naming convention of their choosing, This would also ensure that like files are
# placed near one another (again, assuming alphanumerical sorting applies).


import os
import sys
import shutil
from time import perf_counter


def single_level_dir():
    path = './singleRoot'
    try:
        os.mkdir(path)
        for elem in range(1, 101):
            file_name = 'file' + str(elem) + '.txt'
            fp = open(os.path.join(path, file_name), 'x')
            fp.close()
    except OSError:
        print('your files already exist')
        sys.exit(1)

def hierarchical_level_dir():
    i = 1
    path = './hierarchicalRoot'
    try:
        os.mkdir(path)
        for elem in range(1, 11):                                # create dirs
            dir_name = 'files' + str(i) + '-' + str(i + 9)
            i += 10
            os.makedirs(os.path.join(path, dir_name))
        for elem in range(1, 101):                               # create files
            file_name = 'file' + str(elem) + '.txt'
            fp = open(os.path.join(path, file_name), 'x')
            fp.close()
    except OSError:
        print('your files already exist')
        sys.exit(1)
    for elem in range(1, 101):                                   # loop through dirs and move files
        filename = 'file' + str(elem) + '.txt'
        if elem <= 10:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files1-10')
        elif elem <= 20:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files11-20')
        elif elem <= 30:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files21-30')
        elif elem <= 40:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files31-40')
        elif elem <= 50:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files41-50')
        elif elem <= 60:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files51-60')
        elif elem <= 70:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files61-70')
        elif elem <= 80:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files71-80')
        elif elem <= 90:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files81-90')
        elif elem <= 100:
            shutil.move(os.path.join(path, filename), './hierarchicalRoot/files91-100')


def traverse_single():
    single = []
    for root, dirs, files in os.walk('./singleRoot'):
        for name in files:
            single += [[os.path.join(root, name), os.path.getsize(os.path.join(root, name))]]
    return single


def traverse_hierarchical():
    hierarchical = []
    dirs = []
    for root, sub_dirs, files in os.walk('./hierarchicalRoot'):
        for name in files:
            hierarchical += [[os.path.join(root, name), os.path.getsize(os.path.join(root, name))]]
        for name in sub_dirs:
            dirs += [[os.path.join(root, str(name)), os.path.getsize(os.path.join(root, str(name)))]]
    return dirs, hierarchical


def comp_traversal_time(root):
    if root == './hierarchicalRoot':
        start = perf_counter()
        data_list_hierarchical = traverse_hierarchical()
        stop = perf_counter()
        total_time = ((stop - start) * 1000)                # calc total time (milliseconds)
        return total_time, data_list_hierarchical[0], data_list_hierarchical[1]
    if root == './singleRoot':
        start = perf_counter()
        data_list_single = traverse_single()
        stop = perf_counter()
        total_time = ((stop - start) * 1000)                # calc total time (milliseconds)                                                                                                               # set up data to be returned to main
        return total_time, data_list_single


def main():
    single_root = './singleRoot' # ---------------------------------------------------------- single -------------------
    single_level_dir()
    data_list_single = comp_traversal_time(single_root)
    run_time_single = data_list_single[0]
    data_single = data_list_single[1]
    file_bytes_single = 0
    fp_single = open(os.path.join('./singleRoot', 'singleLevelFiles.txt'), 'a')
    for i in range (0, len(data_single)):
        fp_single.write(str(data_single[i][0]) + ':\t' + str(data_single[i][1]) + 'bytes\n')
        file_bytes_single += data_single[i][1]
    fp_single.close()
    print('Single level file system')
    print('Number of files: ' + str(len(data_single)))
    print('Average file size: ' + str(file_bytes_single / len(data_single)))
    print('Traversal time: ' + str(float("{0:.4f}".format(run_time_single))))
    hierarchical_root = './hierarchicalRoot' # ---------------------------------------------- hierarchical -------------
    hierarchical_level_dir()
    data_list_hierarchical = comp_traversal_time(hierarchical_root)
    run_time_hierarchical = data_list_hierarchical[0]
    data_dirs_hierarchical = data_list_hierarchical[1]
    data_files_hierarchical = data_list_hierarchical[2]
    dir_bytes_hierarchical = 0
    file_bytes_hierarchical = 0
    fp_hierarchical = open(os.path.join('./hierarchicalRoot', 'hierarchicalFiles.txt'), 'a')
    for i in range (0, len(data_dirs_hierarchical)):
        fp_hierarchical.write(str(data_dirs_hierarchical[i][0]) + ': ' + str(data_dirs_hierarchical[i][1]) + 'bytes\n')
        dir_bytes_hierarchical += data_dirs_hierarchical[i][1]
    for i in range (0, len(data_files_hierarchical)):
        fp_hierarchical.write(str(data_files_hierarchical[i][0]) + ': ' + str(data_files_hierarchical[i][1]) + 'bytes\n')
        file_bytes_hierarchical += data_files_hierarchical[i][1]
    fp_hierarchical.close()
    print('\nHierarchical level file system')
    print('Number of directories: ' + str(len(data_dirs_hierarchical)))
    print('Number of files: ' + str(len(data_files_hierarchical)))
    print('Average file size: ' + str(file_bytes_hierarchical / len(data_files_hierarchical)))
    print('Average directory size: ' + str(dir_bytes_hierarchical / len(data_dirs_hierarchical)))
    print('Traversal time: ' + str(float("{0:.4f}".format(run_time_hierarchical))))


if __name__ == "__main__":
    main()
