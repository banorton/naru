import os
import cv2


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if img is not None:
            images.append(img)
    return images
