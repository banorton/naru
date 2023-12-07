import numpy as np
import os
from .funcs import load_images_from_folder
from matplotlib import pyplot as plt
import eng_to_ipa as ipa
from .gui import Gui


class Naru:
    script = "script1"
    naru_vowels = load_images_from_folder(os.getcwd() + f"/naru/{script}/vowels")
    naru_consonants = load_images_from_folder(
        os.getcwd() + f"/naru/{script}/consonants"
    )

    # fmt: off
    ipa_vowels = ['ə', 'ɪ', 'i', 'ɛ', 'æ', 'u', 'e', 'ɑ', 'ɔ', 'o', 'a', 'ʊ']
    ipa_consonants = ['n', 'r', 't', 's', 'd', 'l', 'k', 'ð', 'm', 'z', 'p', 'v', 'w', 'b', 'f', 'h', 'ŋ', 'ʃ', 'j', 'g', 'ʤ', 'ʧ', 'θ', 'ʒ']
    # fmt: on

    @staticmethod
    def translate(txt, syl_lim=5):
        d, lns = Naru.dictionary(), [[]]
        ln = lns[0]
        for word in txt.split():
            word = Naru._prep_word(word)
            phonemes = Naru._prep_phonemes(word)

            # Start syllable and add an open for the word.
            syl = np.ones((27, 27), dtype=np.uint8) * 255
            syl[:, 0:1] = 0

            for p in phonemes:
                mask = d[p] - 255
                syl += mask
                if p in Naru.ipa_vowels:
                    if len(ln) == syl_lim:
                        lns.append([])
                        ln = lns[-1]
                    ln.append(syl)
                    syl = np.ones((27, 27), dtype=np.uint8) * 255
            if any(syl.flatten() == 0):
                if len(ln) == syl_lim:
                    lns.append([])
                    ln = lns[-1]
                ln.append(syl)

            # Add a close to the word.
            close = np.ones((27, 27), dtype=np.uint8) * 255
            close = np.ones(ln[-1].shape, dtype=np.uint8) * 255
            close[:, 26:] = 0
            close -= 255
            ln[-1] += close

            # Add a space between words.
            ln.append(np.ones((27, 8)) * 255)
        Naru._addendspace(lns[-1], syl_lim)
        for i in range(len(lns)):
            lns[i] = np.concatenate(lns[i], axis=1)
            lnspc = np.ones((8, lns[0].shape[1])) * 255
            lns[i] = np.concatenate((lns[i], lnspc), axis=0)
        return np.concatenate(lns, axis=0)

    @staticmethod
    def _prep_word(word):
        return "".join([c.lower() for c in word if c.isalpha()])

    @staticmethod
    def _addendspace(ln, syl_lim):
        for _ in range(syl_lim - len(ln)):
            blank = np.ones((27, 27), dtype=np.uint8) * 255
            ln.append(blank)

    @staticmethod
    def _prep_word(word):
        return "".join([c.lower() for c in word if c.isalpha()])

    @staticmethod
    def _prep_phonemes(word):
        phonemes = ipa.ipa_list(word)
        phonemes = sorted(phonemes[0], key=lambda x: len(x))
        phonemes = phonemes[0]

        phonemes = phonemes.replace("ˈ", "")
        phonemes = phonemes.replace("ˌ", "")
        phonemes = phonemes.replace("*", "")
        return phonemes

    @staticmethod
    def dictionary():
        vlen = min(len(Naru.ipa_vowels), len(Naru.naru_vowels))
        vzip = list(zip(Naru.ipa_vowels[:vlen], Naru.naru_vowels[:vlen]))
        clen = min(len(Naru.ipa_consonants), len(Naru.naru_consonants))
        czip = list(zip(Naru.ipa_consonants[:clen], Naru.naru_consonants[:clen]))
        return dict([entry for entry in vzip] + [entry for entry in czip])

    @staticmethod
    def plot(words, naruwords, title=True):
        arrsz = (len(words) // 2, 2)
        for i in range(len(naruwords)):
            plt.subplot(arrsz[0], arrsz[1], i + 1)
            plt.imshow(naruwords[i], cmap="gray")
            plt.axis("off")
            if title:
                plt.title(words[i])
        plt.show()

    def mkgui():
        gui = Gui()
        gui.root.mainloop()
        return gui
