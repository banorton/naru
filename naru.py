import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
import random as rand


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if img is not None:
            images.append(img)
    return images


def en2naru(txt):
    assert isinstance(txt, str)

    imgs = load_images_from_folder(os.getcwd() + "/imgs/chars")
    img = rand.choice(imgs)
    for char in txt[1:]:
        img = np.concatenate((img, rand.choice(imgs)), axis=1)

    return img


if __name__ == "__main__":
    naru_name = en2naru("brandon")

    plt.imshow(naru_name, cmap="gray")
    plt.axis("off")
    plt.show()
