from gtts import gTTS
import os
import sys


with open(sys.argv[1], "r") as infile:
    lines = infile.readlines()


all_text = "".join(lines)

tts = None

langs = ['en', 'es']
current_lang_index = 0

tts = gTTS(text=all_text, lang=langs[current_lang_index])
tts.save(f"monologue.mp3")

