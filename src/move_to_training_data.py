import os
import shutil

######################################################

# from CONSTANTS import
FRAMES_WITH_LABELS = os.path.join('.', 'frames')   # CHANGE ACCORDINGLY
TRAINING_DATA = os.path.join('.', 'training_data') # CHANGE ACCORDINGLY

######################################################
  

def main():
  # if './frames' does not exist, then exit (no data)
  if not os.path.isdir(FRAMES_WITH_LABELS):
    return

  # if './training_data' does not exist, make it
  # if it does, make sure it is empty
  os.makedirs(TRAINING_DATA, exist_ok = True)

  with os.scandir(TRAINING_DATA) as it:
    if not (next(it, None) is None):
      return

  IMAGES_PREF = os.path.join(TRAINING_DATA, 'images')
  LABELS_PREF = os.path.join(TRAINING_DATA, 'labels')
  IMAGES_TRAIN_PATH = os.path.join(IMAGES_PREF, 'train')
  IMAGES_VAL_PATH = os.path.join(IMAGES_PREF, 'val')
  LABELS_TRAIN_PATH = os.path.join(LABELS_PREF, 'train')
  LABELS_VAL_PATH = os.path.join(LABELS_PREF, 'val')

  os.makedirs(IMAGES_PREF, exist_ok = True)
  os.makedirs(LABELS_PREF, exist_ok = True)
  os.makedirs(IMAGES_TRAIN_PATH, exist_ok = True)
  os.makedirs(IMAGES_VAL_PATH, exist_ok = True)
  os.makedirs(LABELS_TRAIN_PATH, exist_ok = True)
  os.makedirs(LABELS_VAL_PATH, exist_ok = True)

  directory = os.listdir(FRAMES_WITH_LABELS)
  filenames = [file[:-4] for file in directory if file.endswith(".jpg")]

  label_file = ""
  img_file = ""
  copied_counter = 0

  for i in range(len(filenames)):
    item = filenames[i]
    img_file = item + ".jpg"
    label_file = item + ".txt"

    if i % 2 == 0:
      shutil.copy(os.path.join(FRAMES_WITH_LABELS, img_file), os.path.join(IMAGES_TRAIN_PATH, img_file))

      if label_file in directory:
        shutil.copy(os.path.join(FRAMES_WITH_LABELS, label_file), os.path.join(LABELS_TRAIN_PATH, label_file))
        copied_counter += 1
      else:
        with open(os.path.join(LABELS_TRAIN_PATH, label_file), 'a'):
          pass

    else:
      shutil.copy(os.path.join(FRAMES_WITH_LABELS, img_file), os.path.join(IMAGES_VAL_PATH, img_file))

      if label_file in directory:
        shutil.copy(os.path.join(FRAMES_WITH_LABELS, label_file), os.path.join(LABELS_VAL_PATH, label_file))
        copied_counter += 1
      else:
        with open(os.path.join(LABELS_VAL_PATH, label_file), 'a'):
          pass


  print(f'There were {copied_counter} already existing label files, created {len(filenames) - copied_counter} empty ones')

if __name__ == '__main__':
  main()