import cv2
import os
from enum import Enum
import numpy as np
import random
from typing import List

####################################
FRAMES_PATH = os.path.join('.', 'frames')
# AUG_FRAMES_PATH = os.path.join('.', 'aug_frames') # use if you need augmented frames somewhere else
####################################

# Define the image processing functions (from above)
def rotate(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def scale(image, scale_factor, target_dims=None):
    """Scales an image by a given factor or to target dimensions."""
    if target_dims:
        new_w, new_h = target_dims
    else:
        (h, w) = image.shape[:2]
        new_w, new_h = int(w * scale_factor), int(h * scale_factor)
    scaled_img = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return scaled_img

def add_gaussian_noise(image, mean=0, var=0.01):
    image_float = image.astype(np.float32) / 255.0
    sigma = var**0.5
    gaussian = np.random.normal(mean, sigma, image_float.shape)
    noisy_image = image_float + gaussian
    noisy_image = np.clip(noisy_image, 0, 1)
    noisy_image = (noisy_image * 255).astype(np.uint8)
    return noisy_image

def adjust_colour(image, hue_shift=0, saturation_factor=1.0, value_factor=1.0):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    h = (h + hue_shift) % 180
    s = np.clip(s * saturation_factor, 0, 255).astype(np.uint8)
    v = np.clip(v * value_factor, 0, 255).astype(np.uint8)
    adjusted_hsv = cv2.merge([h, s, v])
    adjusted_bgr_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)
    return adjusted_bgr_image

class AugType(Enum):
    ROTATE = 'rotate'
    SCALE = 'scale'
    ADD_NOISE = 'add_noise'
    ADJUST_COLOUR = 'colour_change'

def img_augmentation(image: cv2.typing.MatLike, enum_list: List[AugType]) -> cv2.typing.MatLike:
    new_img = image.copy()
    for enum in enum_list:
        match enum:
            case AugType.ADD_NOISE:
                mean = random.random()/100
                variance = random.random()/100
                print(f"\tApplying noise: mean={mean}, variance={variance}")
                new_img = add_gaussian_noise(new_img, mean, variance)
            case AugType.ADJUST_COLOUR:
                hue_shift = random.randint(0, 10)
                sat_factor = 0.5 * random.random() + 0.5
                val_factor = 0.5 * random.random() + 0.5
                print(f"\tApplying color shift (h,s,v) = ({hue_shift}, {sat_factor}, {val_factor})")
                new_img = adjust_colour(new_img, hue_shift, sat_factor, val_factor)
            case AugType.ROTATE:
                if random.randint(1, 2) % 2 == 0: 
                    angle = random.randrange(-20, 20)
                else:
                    angle = random.randrange(160, 200)
                print(f"\tApplying rotation: {angle} deg")
                new_img = rotate(new_img, angle)
            case AugType.SCALE:
                scale_fac = random.random() + 0.5
                print(f"\tApplying scaling: factor = {scale_fac}")
                new_img = scale(new_img, scale_fac)
    return new_img


def main() -> None:
    # os.makedirs(AUG_FRAMES_PATH, exist_ok = True)

    AUG_COUNT_FACTOR = 0.5 # Determines how much of the input files will be "augmented"

    directory = os.listdir(FRAMES_PATH)
    images_list = [file for file in directory if file.endswith(".jpg")]
    files_to_aug = random.sample(images_list, int(len(images_list) * AUG_COUNT_FACTOR))
    images_to_aug = [(file, cv2.imread(os.path.join(FRAMES_PATH, file))) for file in files_to_aug]
    enums_list = [AugType.ADD_NOISE, AugType.ADJUST_COLOUR, AugType.ROTATE, AugType.SCALE]
    
    for filename, img in images_to_aug:
        print(f'Processing {filename}')
        enums_to_use = random.sample(enums_list, random.randint(1, 4))
        new_img = img_augmentation(img, enums_to_use)
        new_filename = filename[:-4] + '-aug.jpg'
        # when you need separate path for augmented imgs, change prefix below
        cv2.imwrite(os.path.join(FRAMES_PATH, new_filename), new_img)

if __name__ == '__main__':
    main()