##ACZ .DAT packer by Andrei Segal (SegalAndrei @ Twitter and Andreisgl @ Github)
## Based on ACZ DAT_extractor by death_the_d0g (death_the_d0g @ Twitter and deaththed0g @ Github)

from cgi import test
import os
from string import ascii_letters, digits
##import traceback
import textwrap
import shutil
import re

basedir = ''

test_folder = "./0003"

test_output_dat = "out_dat.dat"


def check_files():
    ##Get working directory path
    basedir = os.getcwd()

    file_list = []
    file_name = []
    for f in os.listdir(basedir):
        path = os.path.join(basedir, f)
        if os.path.isdir(f):
            file_list.append(path)
            file_name.append(os.path.splitext(f)[0])




def create_header(curr_container_folder):
    num_of_files = len( os.listdir(curr_container_folder) )
    file_size_list = []
    # Point to .zof file
    zof_file = curr_container_folder + '.zof'

    # Get file sizes for header
    for file in os.listdir(curr_container_folder):
        path = os.path.join(curr_container_folder, file)
        file_size_list.append(os.path.getsize(path))
    
    # Add old '0' offsets from original file through .zof file
    with open(zof_file, 'rb') as ZOF:
        zof_size = os.path.getsize(zof_file)
        for offset in range(int(zof_size /4)):
            data = int.from_bytes(ZOF.read(4), byteorder = "little")
            file_size_list.insert( int(data), 0 )
    
    print('end')



#check_files()
create_header(test_folder)
