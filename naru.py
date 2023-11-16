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
    def translate(txt):
        d = naru.dictionary()
        splt = txt.split()
        naru_txt = []
        for word in splt:
            word = naru._prep_word(word)
            phonemes = naru._prep_phonemes(word)
            print(phonemes)
            buffer = np.ones((27, 27), dtype=np.uint8) * 255
            buffer[:, 0:2] = 0
            for p in phonemes:
                print(p)
                mask = d[p] - 255
                buffer += mask
                if p in naru.ipa_vowels:
                    naru_txt.append(buffer)
                    buffer = np.ones((27, 27), dtype=np.uint8) * 255
            if any(buffer.flatten() == 0):
                naru_txt.append(buffer)
            stop = np.ones((27, 27), dtype=np.uint8) * 255
            stop[:, 25:] = 0
            stop -= 255
            naru_txt[-1] += stop
            naru_txt.append(np.ones((27, 4)) * 255)
        return np.concatenate(tuple(naru_txt), axis=1)

    @staticmethod
    def _prep_word(word):
        return "".join([c.lower() for c in word if c.isalpha()])

    @staticmethod
    def _prep_word(word):
        return "".join([c.lower() for c in word if c.isalpha()])

    @staticmethod
    def _prep_phonemes(word):
        # phonemes = ipa.convert(word)

        phonemes = ipa.ipa_list(word)
        phonemes = sorted(phonemes[0], key=lambda x: len(x))
        phonemes = phonemes[0]

        phonemes = phonemes.replace("ˈ", "")
        phonemes = phonemes.replace("ˌ", "")
        return phonemes

    @staticmethod
    def dictionary():
        vlen = min(len(naru.ipa_vowels), len(naru.naru_vowels))
        vzip = list(zip(naru.ipa_vowels[:vlen], naru.naru_vowels[:vlen]))
        clen = min(len(naru.ipa_consonants), len(naru.naru_consonants))
        czip = list(zip(naru.ipa_consonants[:clen], naru.naru_consonants[:clen]))
        return dict([entry for entry in vzip] + [entry for entry in czip])


if __name__ == "__main__":
    naruword1 = naru.translate("The quick brown fox jumps over the lazy dog")
    naruword2 = naru.translate("Ana")
    plt.subplot(311)
    plt.imshow(naruword1, cmap="gray")
    plt.axis("off")
    plt.subplot(312)
    plt.imshow(naruword2, cmap="gray")
    plt.axis("off")
    plt.show()

    # print(len(naru.naru_vowels))
    # print(len(naru.naru_consonants))
    # print(len(naru.ipa_vowels))
    # print(len(naru.ipa_consonants))
