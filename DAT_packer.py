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

output_dat = "out_dat.dat"


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
    offset_list = []
    # Point to .zof file
    zof_file = curr_container_folder + '.zof'

    # Get file sizes for header
    for file in os.listdir(curr_container_folder):
        path = os.path.join(curr_container_folder, file)
        file_size_list.append(os.path.getsize(path))
    
    # Create offset list. (WILL BE OFFSET LATER ACCORDING TO HEADER LENGTH!)
    offset_list.append(0)
    for index in range(len(file_size_list)):
        offset_list.append(file_size_list[index] + offset_list[index])
    

    header_length = (len(offset_list) + 1) * 4
    for index in range(len(offset_list)):
        offset_list[index] += header_length
    
    offset_list.insert(0, len(offset_list))

    
    
    # Add total size to beginning of list
    file_size_list.insert(0, len(file_size_list))

    # Add old '0' offsets from original file through .zof file
    with open(zof_file, 'rb') as ZOF:
        zof_size = os.path.getsize(zof_file)
        for offset in range(int(zof_size /4)):
            data = int.from_bytes(ZOF.read(4), byteorder = "little")
            offset_list.insert( int(data) +1, 0 )
    offset_list.pop()
    
    #with open(test_output_dat, 'wb') as OD:
    #    for item in offset_list:
    #        xx = item.to_bytes(byteorder="little", length=4)
    #        OD.write(xx)

    return offset_list
        
# Packs the file. Receives current container and destination file.
def pack_files(curr_container_folder, output_file):
    # Get header values
    header_list = create_header(curr_container_folder)

    with open(output_file, 'wb') as OF:
        # Write header to file
        for item in header_list:
            OF.write(item.to_bytes(byteorder="little", length=4))
        
        for f in os.listdir(curr_container_folder):
            path = os.path.join(curr_container_folder, f)
            with open(path, 'rb') as infile:
                OF.write(infile.read())
            




check_files()

pack_files(test_folder, output_dat)
print("end")
