# Naru Translator: A Phonetically Consistent Orthography for English

## Overview

The Naru Translator is a Python application that converts English text into a phonetically consistent orthography called "Naru." English, unlike phonetically consistent languages such as Spanish or German, has a complex relationship between spelling and pronunciation. Words like "to," "too," and "two," or "there," "their," and "they're" are spelled differently but pronounced the same, indicating that certain characters have varying sounds depending on context. 

Naru resolves this inconsistency by assigning each English phoneme a unique character. This creates a phonetically consistent orthography for English. The Naru characters are designed to allow consonants and vowels to be layered over each other, creating a unique symbol for each syllable. This structure enables Naru to function as a syllabic orthography, similar to Japanese. Additionally, the most common English phonemes are mapped to the simplest characters in Naru, making the script easier to write and read.

Each character in the Naru script is a 27x27 pixel, 8-bit image, designed to represent a unique English phoneme. The translation process involves breaking down input text into words, converting them into phonemes, and generating a visual representation using the Naru script.

## Project Description

This project implements a compiler/interpreter for the Naru language, focusing on tokenization, parsing, and evaluation phases to convert English into Naru script. The project includes a GUI for easy interaction and displays translated English text as a Naru image.

### Key Components

1. **Naru Script**: A unique, syllabic script for English phonemes, where each phoneme has a distinct character.
2. **Phoneme Mapping**: Maps English IPA phonemes to Naru characters, allowing for consistent phonetic representation.
3. **Translation Pipeline**: Converts English text to IPA phonemes, matches them with Naru characters, and arranges them into syllables and lines.
4. **Graphical User Interface (GUI)**: A `tkinter`-based interface allowing users to input English text, translate it to Naru, and view the visual output.

### Features

- **Phonetic Consistency**: Ensures a one-to-one mapping of phonemes to characters, achieving phonetic consistency for English.
- **Interactive GUI**: Users can input English text, click "Translate," and view it in Naru script.
- **Image Processing**: Uses `numpy` to construct the visual output, syllable by syllable.
- **Customizable Script**: Users can choose different Naru scripts, each providing unique character representations for phonemes.
- **Concatenated Output**: Arranges syllables and words in lines, automatically handling line breaks when reaching space limits.

### Technologies Used

- **NumPy**: For handling image arrays and processing.
- **Tkinter**: For the GUI, creating an interactive experience.
- **Matplotlib**: Renders the Naru script images within the GUI.
- **eng_to_ipa**: Converts English text to its IPA (International Phonetic Alphabet) phonetic representation.

This project provides a novel way to visualize English text phonetically, enabling users to experience English in a syllabic, phonetic script that is easy to read and consistent in sound.
