import tkinter as tk
from tkinter import ttk
from os import path
from math import floor


class Gui:
    def __init__(self, parent=None):
        self.parent = parent
        root = tk.Tk()
        self.root = root
        root.geometry("800x600")
        root.resizable(width=False, height=False)
        root.title("Naru")
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        style = ttk.Style(root)
        root.tk.call("source", path.join(path.dirname(__file__), "forest-dark.tcl"))
        style.theme_use("forest-dark")

        # Top Frame
        translate_eng = ttk.Frame(root)
        translate_eng_label = ttk.Label(
            translate_eng,
            text="English",
            font="Helvetica 18 bold",
            width=8,
            anchor="e",
        )
        translate_eng_label.pack(side="left", padx=5)
        translate_eng_text = tk.Text(translate_eng)
        translate_eng_text.pack(side="right", fill="both", pady=5)
        translate_eng.grid(row=0, column=0, padx=10)

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
        translate_naru_text = tk.Text(translate_naru)
        translate_naru_text.pack(side="right", fill="both", pady=5)
        translate_naru.grid(row=1, column=0, padx=10)
