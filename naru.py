import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
import random as rand
import eng_to_ipa as ipa


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if img is not None:
            images.append(img)
    return images


class naru:
    naru_vowels = load_images_from_folder(os.getcwd() + "/script2/vowels")
    naru_consonants = load_images_from_folder(os.getcwd() + "/script2/consonants")

    # fmt: off
    ipa_vowels = ['ə', 'ɪ', 'i', 'ɛ', 'æ', 'u', 'e', 'ɑ', 'ɔ', 'o', 'a', 'ʊ']
    ipa_consonants = ['n', 'r', 't', 's', 'd', 'l', 'k', 'ð', 'm', 'z', 'p', 'v', 'w', 'b', 'f', 'h', 'ŋ', 'ʃ', 'j', 'g', 'ʤ', 'ʧ', 'θ', 'ʒ']
    # fmt: on

    @staticmethod
    def en2naru(txt):
        return None

    @staticmethod
    def dictionary():
        vlen = min(len(naru.ipa_vowels), len(naru.naru_vowels))
        vzip = list(zip(naru.ipa_vowels[:vlen], naru.naru_vowels[:vlen]))

        clen = min(len(naru.ipa_consonants), len(naru.naru_consonants))
        czip = list(zip(naru.ipa_consonants[:clen], naru.naru_consonants[:clen]))

        return [entry for entry in vzip] + [entry for entry in czip]


if __name__ == "__main__":
    print(naru.dictionary())
    # naru_name = en2naru("brandon")
    # plt.imshow(naru_name, cmap="gray")
    # plt.axis("off")
    # plt.show()

    # print(len(naru.naru_vowels))
    # print(len(naru.naru_consonants))
    # print(len(naru.ipa_vowels))
    # print(len(naru.ipa_consonants))
