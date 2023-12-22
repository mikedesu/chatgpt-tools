import gtts

for lang in gtts.lang.tts_langs():
    print(lang, gtts.lang.tts_langs()[lang])
