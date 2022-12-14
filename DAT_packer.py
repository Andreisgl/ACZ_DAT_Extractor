##ACZ .DAT packer by Andrei Segal (SegalAndrei @ Twitter and Andreisgl @ Github)
## Based on ACZ DAT_extractor by death_the_d0g (death_the_d0g @ Twitter and deaththed0g @ Github)

from cgi import test
from email import header
import os
from string import ascii_letters, digits
##import traceback
import textwrap
import shutil
import re



basedir = ""
folder_path_list = []
folder_list = []
zof_folder = "zof"

ignore_folder_list = [".git", zof_folder] # Hardcoded folders to ignore AKA ".git" is annoying

def check_files():
    ##Get working directory path
    global basedir
    basedir = os.getcwd()

    global zof_folder
    zof_folder = basedir + "/" + zof_folder

    
    for f in os.listdir(basedir):
        path = os.path.join(basedir, f)
        if os.path.isdir(f):
            if not f in ignore_folder_list:
                folder_path_list.append(path)
                folder_list.append(os.path.splitext(f)[0])


def create_header(curr_container_folder):
    num_of_files = len( os.listdir(curr_container_folder) )
    file_size_list = []
    offset_list = []
    # Point to .zof file
    
    zof_file = zof_folder + "/" + curr_container_folder + '.zof'

    # Get file sizes for header
    for file in os.listdir(curr_container_folder):
        path = os.path.join(curr_container_folder, file)
        file_size_list.append(os.path.getsize(path))
    
    # Create offset list. (WILL BE OFFSET LATER ACCORDING TO HEADER LENGTH!)
    offset_list.append(0)
    for index in range(len(file_size_list)):
        offset_list.append(file_size_list[index] + offset_list[index])
    
    #Check .zof file to know how many header positions are missing
    try:
        with open(zof_file, 'rb') as ZOF:
            additional_zeros_in_header = int(os.path.getsize(zof_file) /4)         
    except:
        print(".zof size check exception!:  " + curr_container_folder)

    # If header doesn't complete the last 16-byte line, add padding
    # to the end of the list
    header_length = ((len(offset_list)) + additional_zeros_in_header) * 4
    if header_length % 16 != 0:
        # Number of bytes to be added to the list at the end of the process
        padding_length = int(((16 * (int(header_length/16) + 1)) - header_length) /4)
        header_length += padding_length*4 # Add padding to header size
    
    # Add header length to all values to display the real values of the final file
    for index in range(len(offset_list)):
        offset_list[index] += header_length
    
    try:
        # Add old missing '0' offsets from original file through .zof file
        with open(zof_file, 'rb') as ZOF:
            zof_size = os.path.getsize(zof_file) # Get file size and...
            for offset in range(int(zof_size /4)): # ...get the number of offsets present in file
                data = int.from_bytes(ZOF.read(4), byteorder = "little") # Read position of 0 offset
                offset_list.insert( int(data), 0 ) # Insert 0 in the required position
    except:
        print(".zof exception!:  " + curr_container_folder)

    offset_list.pop()
    offset_list.insert(0, len(offset_list))

    # Add padding to end of the list
    for i in range(padding_length):
        offset_list.append(0)
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

for folder in folder_list:
    pack_files(folder, folder + ".dat")
print("end")
