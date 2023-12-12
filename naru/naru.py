import numpy as np
import os
from os import path
from .funcs import load_images_from_folder
from matplotlib import pyplot as plt
import eng_to_ipa as ipa
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import floor, sqrt


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
    def translate(txt):
        d, lns = Naru.dictionary(), [[]]
        ln = lns[0]
        ln_len = 0
        words = txt.split()
        syl_lim = floor(sqrt(len(words) * 3))
        for word in words:
            word = Naru._prep_word(word)
            phonemes = Naru._prep_phonemes(word)

            # Start syllable and add an open for the word.
            syl = np.ones((27, 27), dtype=np.uint8) * 255
            syl[:, 0:1] = 0
            for p in phonemes:
                mask = d[p] - 255
                syl += mask
                if p in Naru.ipa_vowels:
                    if (syl_lim * 27) - ln_len < 27:
                        Naru._addendspace(lns[-1], syl_lim, ln_len)
                        lns.append([])
                        ln = lns[-1]
                        ln_len = 0
                    ln.append(syl)
                    ln_len += 27
                    syl = np.ones((27, 27), dtype=np.uint8) * 255
            if any(syl.flatten() == 0):
                if (syl_lim * 27) - ln_len < 27:
                    Naru._addendspace(lns[-1], syl_lim, ln_len)
                    lns.append([])
                    ln = lns[-1]
                    ln_len = 0
                ln.append(syl)
                ln_len += 27

            # Add a close to the word.
            close = np.ones((27, 27), dtype=np.uint8) * 255
            close = np.ones(ln[-1].shape, dtype=np.uint8) * 255
            close[:, 26:] = 0
            close -= 255
            ln[-1] += close

            # Add a space between words. Start new line if not enough space.
            if (syl_lim * 27) - ln_len >= 27:
                ln.append(np.ones((27, 8)) * 255)
                ln_len += 8
            elif (syl_lim * 27) - ln_len < 27:
                Naru._addendspace(lns[-1], syl_lim, ln_len)
                lns.append([])
                ln = lns[-1]
                ln_len = 0

        Naru._addendspace(lns[-1], syl_lim, ln_len)
        for i in range(len(lns)):
            if len(lns[i]) == 0:
                continue
            lns[i] = np.concatenate(lns[i], axis=1)
            lnspc = np.ones((8, lns[0].shape[1])) * 255
            lns[i] = np.concatenate((lns[i], lnspc), axis=0)
        return np.concatenate(lns, axis=0)

    @staticmethod
    def _prep_word(word):
        return "".join([c.lower() for c in word if c.isalpha()])

    @staticmethod
    def _addendspace(ln, syl_lim, ln_len):
        width_needed = (syl_lim * 27) - ln_len
        blank = np.ones((27, width_needed), dtype=np.uint8) * 255
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
    def plot(naru_words, fig, ax):
        if not fig or not ax:
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.imshow(naru_words, cmap="gray")
            ax.axis("off")
            return fig, ax
        elif fig and ax:
            ax.clear()
            ax.imshow(naru_words, cmap="gray")
            ax.axis("off")
            return fig, ax

    @staticmethod
    def mkgui():
        gui = Gui()
        gui.root.mainloop()
        return gui


class Gui:
    def __init__(self, parent=None):
        self.parent = parent
        self.curr_plt = None
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot()
        root = tk.Tk()
        self.root = root
        root.geometry("800x800")
        root.resizable(width=False, height=False)
        root.title("Translator")
        root.rowconfigure(0, weight=10)
        root.rowconfigure(1, weight=1)
        style = ttk.Style(root)
        root.tk.call("source", path.join(path.dirname(__file__), "forest-dark.tcl"))
        style.theme_use("forest-dark")

        # Top Frame
        translate_eng = ttk.Frame(root)
        info_frame = ttk.Frame(translate_eng)
        translate_eng_label = ttk.Label(
            info_frame,
            text="English",
            font="Helvetica 18 bold",
            width=8,
            anchor="e",
        )
        translate_eng_label.pack(side="top", padx=5)
        translate_btn = ttk.Button(
            info_frame, text="Translate", command=self.translate_and_plot
        )
        translate_btn.pack(side="bottom", pady=5)
        info_frame.pack(side="left")
        translate_eng_text = tk.Text(translate_eng)
        translate_eng_text.pack(side="right", fill="both", pady=5)
        translate_eng_text.focus()
        translate_eng.grid(row=0, column=0, padx=5)
        self.entry = translate_eng_text

        # Bottom Frame
        translate_naru = ttk.Frame(root)
        translate_naru_label = ttk.Label(
            translate_naru,
            text="Naru",
            font="Helvetica 18 bold",
            width=8,
            anchor="e",
        )
        translate_naru_label.pack(side="left", padx=5)
        naru_text_frame = ttk.Frame(translate_naru)
        self.naru_frame = naru_text_frame
        naru_text_frame.pack(side="right", padx=5)
        translate_naru.grid(row=1, column=0, padx=5)

    def translate_and_plot(self):
        # self._clear_plt()
        if self.curr_plt == None:
            print("hello")
            txt = self.entry.get("1.0", "end-1c")
            naru_txt = Naru.translate(txt)
            self.fig, self.axes = Naru.plot(naru_txt, self.fig, self.axes)
            self.curr_plt = FigureCanvasTkAgg(self.fig, master=self.naru_frame)
            self.curr_plt.draw()
            self.curr_plt.get_tk_widget().pack()
        else:
            print("world")
            txt = self.entry.get("1.0", "end-1c")
            naru_txt = Naru.translate(txt)
            self.fig, self.axes = Naru.plot(naru_txt, self.fig, self.axes)
            self.curr_plt.draw()

    def _clear_plt(self):
        if self.curr_plt == None:
            return
        self.axes.clear()
