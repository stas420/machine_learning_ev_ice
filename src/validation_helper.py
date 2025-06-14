from ultralytics import YOLO
import cv2
import os

################################################

# from CONSTANTS import
MODEL_PATH = os.path.join('.', 'best.pt') # overwrite if needed
INPUT_DIR = os.path.join('.', 'frames_test') # CHANGE ACCORDINGLY
OUTPUT_DIR = os.path.join('.', 'results') # CHANGE ACCORDINGLY

################################################


model = YOLO(MODEL_PATH)
os.makedirs(OUTPUT_DIR, exist_ok=True)

if os.path.isdir(INPUT_DIR):
    # for each file, check if it's a jpg and pass it to the model
    for fname in os.listdir(INPUT_DIR):
        if not fname.endswith(".jpg"):
            continue
        path = os.path.join(INPUT_DIR, fname)
        img = cv2.imread(path)
        results = model(img)

        # for each 'box' in obtained result write a frame around the found object
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]
            class_id = int(box.cls)
            label = model.names[class_id]
            color = (0,255,0) # if label == "green" else (255,0,0)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imwrite(os.path.join(OUTPUT_DIR, fname), img)

if os.path.isfile(INPUT_DIR):
    if INPUT_DIR.endswith(".jpg"):
        img = cv2.imread(INPUT_DIR)
        results = model(img)

        # for each 'box' in obtained result write a frame around the found object
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]
            class_id = int(box.cls)
            label = model.names[class_id]
            color = (0,255,0) # if label == "green" else (255,0,0)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imwrite(os.path.join(OUTPUT_DIR, 'res-' + INPUT_DIR), img)