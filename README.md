# chatgpt-tools

A collection of tools I am writing and dabbling with that uses ChatGPT's API.

- [https://www.evildojo.com](https://www.evildojo.com)
- [Twitter](https://www.twitter.com/evildojo666)
- [Twitch](https://www.twitch.tv/evildojo666)
- [Youtube](https://www.youtube.com/@evildojo666)

---

### Examples

Probably the most useful immediately is the CLI to ChatGPT. You'll need to switch out your `OPENAI_ORG` and `OPENAI_API_KEY` environment variables to make this work. 

```
python3 pa.py <model> <prompt_filename>
```

```
git clone https://github.com/mikedesu/chatgpt-tools.git
python3 pa.py gpt3.5 coder.txt
```


[![asciicast](https://asciinema.org/a/3AviNnbVq27NTboeUfKndZwq2.svg)](https://asciinema.org/a/3AviNnbVq27NTboeUfKndZwq2)

---

Next is the audio transcription feature that allows you to upload an audio file to OpenAI's "Whisper" API and get back a text file containing the audio transcribed as plaintext.

```
python3 whisper.py <filename> <outfile>
```

[![asciicast](https://asciinema.org/a/xcGyupY0vqEuicqybO93skyE9.svg)](https://asciinema.org/a/xcGyupY0vqEuicqybO93skyE9)

