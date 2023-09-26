# This script unpacks AC5 and ACZ's .dat files
# Based on deaththed0g's script, rewriten by Andrei Segal

import os
import re
import shutil
from string import ascii_letters, digits

def procedure(input_file, destination_folder):
    start_offset = 0
    goto = 0
    with open(input_file, "rb") as inf:
        file_size_check = inf.seek(0, os.SEEK_END)
        inf.seek(0, 0)
        dat_type_check = inf.read(32)
        if dat_type_check == b"\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            goto = 32
        else:
            goto = 0
        inf.seek(goto, 0)
        dat_type_check = inf.read(16)
        dat_type_array = re.compile(b'\x10\x00\x00\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        if (re.match(dat_type_array, dat_type_check)):
            print("ext type 2!")
        else:
            inf.seek(0, 0)
            nof = int.from_bytes(inf.read(4), "little")
            file_size_check = inf.seek(0, os.SEEK_END)
            if nof <= 0 or nof >= file_size_check:
                pass
            else:
                extraction1(inf)

def extraction1(dat_ext, nof):
    dat_ext.seek(0,0)
    nof = int.from_bytes(dat_ext.read(4), "little")
    pass


procedure("0347.dat", "aa")