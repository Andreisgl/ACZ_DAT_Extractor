##ACZ string decode by death_the_d0g (death_the_d0g @ Twitter and deaththed0g @ Github)

import os
from string import ascii_letters, digits
##import traceback
import textwrap
import shutil
import re
import sys

def dat_ext_type1(*args):
    try:
        
        print("running dat_ext_type1")
        current_filename = args[1]
        start_offset = args[2]
        file_offsets = []
        file_sizes = []

        zero_offset_list = []
        zof_folder = "zof"
        zero_offset_file = "./" + zof_folder + "/" + current_filename + ".zof"
        if not os.path.exists(zof_folder):
            os.mkdir(zof_folder)

        dat_ext.seek(start_offset, 0)
        nof = int.from_bytes(dat_ext.read(4), "little")
        for x in range(nof):
            f_offset = dat_ext.read(4)
            file_offsets.append(int.from_bytes(f_offset, "little") + start_offset)

        search_start = 0
        for i in range(file_offsets.count(0)): #Count occurrences of 0 in file_offsets
            current_zero_offset = file_offsets.index(0, search_start)
            zero_offset_list.append(current_zero_offset)
            search_start = current_zero_offset + 1
            nof -= 1
            
        while 0 in file_offsets: # Remove all 0 offsets from file_offsets list
            current_zero_offset = file_offsets.index(0)
            file_offsets.pop(current_zero_offset)

        file_offsets.append(file_size_check)
        if os.path.isdir(current_filename):
            shutil.rmtree(current_filename)
        extracted_folder_name = str(current_filename)
        os.mkdir(extracted_folder_name)
        file_number = 0
        sub_itir = 0
        for x in range(nof):
            dat_ext.seek(file_offsets[sub_itir])
            file_ext = dat_ext.read(3)
            file_ext_decoded = file_ext.decode('UTF-8', errors='ignore')
            if set(file_ext_decoded).difference(ascii_letters + digits) or (len(file_ext_decoded) < 3):
                file_extension = "unk"
            else:
                file_extension = str(file_ext_decoded).lower()
            filename = str(current_filename) + "//" + str(file_number).zfill(4) + "." + file_extension
            extracted_file = open(filename, "wb")
            dat_ext.seek(file_offsets[sub_itir])
            file_size = file_offsets[sub_itir + 1] - file_offsets[sub_itir]
            data = dat_ext.read(file_size)
            extracted_file.write(data)
            extracted_file.close()
            file_number += 1
            sub_itir += 1

            with open(zero_offset_file, 'wb') as ZOF:
                for element in zero_offset_list:
                    ZOF.write(element.to_bytes(byteorder="little", length=4))

        return None
    except Exception as error:
        print(current_filename, "error")
        extracted_file.close()
        shutil.rmtree(extracted_folder_name)
        return None

def dat_ext_type2(*args):
    try:
        print("running dat_ext_type2")
        dat_ext.seek(0, 0)
        current_filename = args[1]
        file_offset1 = int.from_bytes(dat_ext.read(4), "little")
        file_offset2 = int.from_bytes(dat_ext.read(4), "little")
        file_offset3 = args[2]
        small_file_offset_list = [file_offset1, file_offset2, file_offset3]
        if os.path.isdir(current_filename):
            shutil.rmtree(current_filename)
        extracted_folder_name = str(current_filename)
        os.mkdir(extracted_folder_name)
        file_number = 0
        sub_itir = 0
        for x in range(2):
            dat_ext.seek(small_file_offset_list[sub_itir])
            file_ext = dat_ext.read(3)
            file_ext_decoded = file_ext.decode('UTF-8', errors='ignore')
            if set(file_ext_decoded).difference(ascii_letters + digits) or (len(file_ext_decoded) < 3):
                file_extension = "unk"
            else:
                file_extension = str(file_ext_decoded).lower()
            filename = str(current_filename) + "//" + str(file_number).zfill(4) + "." + file_extension
            extracted_file = open(filename, "wb")
            file_size = small_file_offset_list[sub_itir + 1] - small_file_offset_list[sub_itir]
            dat_ext.seek(small_file_offset_list[sub_itir])
            data = dat_ext.read(file_size)
            extracted_file.write(data)
            extracted_file.close()
            file_number += 1
            sub_itir += 1
        return None
    except Exception as error:
        print(current_filename, "error")
        extracted_file.close()
        shutil.rmtree(extracted_folder_name)
        return None 

def get_paths(arg_list):
    # Gets .PAC and Extract Folder paths from command line arguments
    global input_path
    #global tbl_path
    global output_path
    global path
    if len(arg_list) == 1: #If no arguments are passed...
        # Use standard values
        path = os.path.join(basedir, f)

    elif len(arg_list) == 3: # If the right ammount of arguments is passed...
        #Get values from list
        input_path = arg_list[1]
        #tbl_path = os.path.splitext(input_path)[0] + ".TBL"
        output_path = arg_list[2]

        path = input_path
        
    
    else: #If none of those conditions are met
        err_msg = "Wrong parameters!"
        exit(err_msg) # Exit program with an error

    
##Get working directory path
basedir = os.getcwd()



##Get DAT files in working directory and and store their location aswell their filenames in arrays
file_list = []
file_name = []
for f in os.listdir(basedir):
    path = os.path.join(basedir, f)
    if f.endswith(".dat") or f.endswith(".DAT") or f.endswith(".unk"):
        file_list.append(path)
        file_name.append(os.path.splitext(f)[0])
    else:
        pass

get_paths(sys.argv)

## Open files, check for dat_type then proceed with the extraction routine
i = 0
for files in file_list:
    start_offset = 0
    goto = 0
    dat_ext = open(file_list[i], "rb")
    current_filename = file_name[i]
    file_size_check = dat_ext.seek(0, os.SEEK_END)
    dat_ext.seek(0, 0)
    dat_type_check = dat_ext.read(32)
    if dat_type_check == b"\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
        goto = 32
    else:
        goto = 0
    dat_ext.seek(goto, 0)
    dat_type_check = dat_ext.read(16)
    dat_type_array = re.compile(b'\x10\x00\x00\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    if (re.match(dat_type_array, dat_type_check)):
        dat_ext_type2(dat_ext, current_filename, file_size_check)
        i += 1
    else:
        dat_ext.seek(0, 0)
        nof = int.from_bytes(dat_ext.read(4), "little")
        file_size_check = dat_ext.seek(0, os.SEEK_END)
        if nof <= 0 or nof >= file_size_check:
            i += 1
            pass
        else:
            dat_ext_type1(dat_ext, current_filename, start_offset)
            i += 1
