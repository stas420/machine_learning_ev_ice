import cv2
import os
from datetime import datetime as dt

#############################################

# from CONSTANTS import
VIDEOS_PATH = 'videos' # CHANGE ACCORDINGLY
FRAMES_PATH = 'frames' # CHANGE ACCORDINGLY

#############################################


TIMESTAMP = dt.now().strftime("%d%m%Y%H%M%S")

# function which takes a .mp4 file and extracts its frames,
# then saves them as images in the provided directory
def extract_frames(video_dir: str, video_name:str, output_dir: str) -> None:
    cap = cv2.VideoCapture(os.path.join(video_dir, video_name))
    saved = 0
    output_prefix = os.path.join(output_dir, TIMESTAMP + '-' + video_name[:-4])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        else:
            frame_path = output_prefix + '-' + f"frame_{saved:03d}.jpg" #os.path.join(output_dir, f"frame_{saved:03d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved += 1
    cap.release()

def is_dir_empty(path: str):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok = True)
    with os.scandir(path) as it:
        return next(it, None) is None

# image extraction
if is_dir_empty(FRAMES_PATH): # pro forma, to not let extract if there are any leftovers
    for x in os.listdir(VIDEOS_PATH):
       extract_frames(VIDEOS_PATH, x, FRAMES_PATH)