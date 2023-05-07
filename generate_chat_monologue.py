from gtts import gTTS
import os
import sys


infilename = sys.argv[1]
outfilename = sys.argv[2]
lang = sys.argv[3]

with open(infilename, "r") as infile:
    lines = infile.readlines()

all_text = "".join(lines)

tts = None


tts = gTTS(text=all_text, lang=lang)
tts.save(outfilename)

