import os
import shutil

########################################
RANGE_START_INCL = 1401 # CHANGE ACCORDINGLY
RANGE_END_INCL = 2100 # CHANGE ACCORDINGLY
########################################

SOURCE_DIR = os.path.join('.', 'frames_all')
DEST_DIR = os.path.join('.', 'frames')

file_list = os.listdir(SOURCE_DIR)
file_list.sort()
N = len(file_list)

if (N < RANGE_END_INCL):
    print(f'Range end is bigger than the file list, new range end is {N}')
    RANGE_END_INCL = N

os.makedirs(DEST_DIR, exist_ok = True)

for i in range(RANGE_START_INCL, RANGE_END_INCL + 1):
    shutil.copyfile(os.path.join(SOURCE_DIR, file_list[i]), os.path.join(DEST_DIR, file_list[i]))
    print(f'Copied file number {i}')

print('Copying ended')