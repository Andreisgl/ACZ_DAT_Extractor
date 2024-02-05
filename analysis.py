import csv
import os

everything = os.listdir()
files = []
dirs = []
rejects = []

for item in everything:
    if(
        os.path.isdir(item)
        and item != 'zof'
        ):

        print('{}: dir'.format(item))
        files.append(item)

    elif(
        os.path.isfile(item)
        and item != '.git'
        and item.split('.')[1] == 'dat'
        ):

        print('{}: file'.format(item))
        dirs.append(item)
    
    else:
        rejects.append(item)



dummy = ['1', '2', '3', '5']

int_current = 0
sanitized_list = []

for lul in dummy:
    try:
        int_current = int(lul)
        sanitized_list.append(int_current)
    except:
        print('not a number!')

worklist = sanitized_list
for index, number in enumerate(worklist):
    difference = worklist[index] == worklist[index+1]
    if difference == 1:
        print('Is continuous') # Next index is more than 1 over current index
    else:
        for d in range(difference):
            pass ### ADD FILES HERE






pass