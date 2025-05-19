from ultralytics import YOLO
import cv2
import os

model = YOLO("models/license_plate.pt")
input_dir = "data/frames"
output_dir = "results/detected"
os.makedirs(output_dir, exist_ok=True)

def is_green_plate(plate_img):
    hsv = cv2.cvtColor(plate_img, cv2.COLOR_BGR2HSV)
    h, s, _ = hsv.mean(axis=0).mean(axis=0)
    return 35 < h < 85 and s > 40

for fname in os.listdir(input_dir):
    if not fname.endswith(".jpg"):
        continue
    path = os.path.join(input_dir, fname)
    img = cv2.imread(path)
    results = model(img)

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = img[y1:y2, x1:x2]
        label = "ZIELONA" if is_green_plate(crop) else "Zwykła"
        color = (0,255,0) if label == "ZIELONA" else (255,0,0)

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imwrite(os.path.join(output_dir, fname), img)
