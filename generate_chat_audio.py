from gtts import gTTS
import os



with open("dialogue00.txt", "r") as infile:
    lines = infile.readlines()


tts = None

langs = ['en', 'es']
current_lang_index = 0

for i in range(len(lines)):
    line = lines[i]
    tts = gTTS(text=lines[i], lang=langs[current_lang_index])
    tts.save(f"out{i}.mp3")
    print(f"saved {i}")
    current_lang_index += 1
    if current_lang_index >= len(langs):
        current_lang_index = 0

with open("files.txt", "w") as outfile:
    for i in range(len(lines)):
        cwd = os.getcwd()
        filepath = f"{cwd}/out{i}.mp3"
        outline = f"file '{filepath}'\n"
        outfile.write(outline)
