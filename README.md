# chatgpt-tools

A collection of tools I am writing and dabbling with that uses ChatGPT's API.

- [https://www.evildojo.com](https://www.evildojo.com)

### Warning

- Use the `autogpt_test.py` (and future tools) program at your own peril.
- One thing not discussed about AutoGPT-type tools is how many requests they make.
- After weeks of not-using the OpenAI API much and then one day deciding to play with an idea, I'd suddenly burnt up a ton of tokens.
- It is important to be mindful of how much content you send per message. 
- Sometimes it is necessary to send previous messages and responses, but each message done this way expontentially increases the content sent.

**Using AutoGPT-type tools can be expensive!!!**

### Examples

Probably the most useful immediately is the CLI to ChatGPT. You'll need to switch out your `organization` and `API_KEY` variables to make this work.

```
python3 pal.py <prompt_filename> <model>
```

[![asciicast](https://asciinema.org/a/bQu9yPcl3T4g1MUVt8MMiL9rC.svg)](https://asciinema.org/a/bQu9yPcl3T4g1MUVt8MMiL9rC)

---

Next is the audio transcription feature that allows you to upload an audio file to OpenAI's "Whisper" API and get back a text file containing the audio transcribed as plaintext.

```
python3 whisper.py <filename> <outfile>
```

[![asciicast](https://asciinema.org/a/xcGyupY0vqEuicqybO93skyE9.svg)](https://asciinema.org/a/xcGyupY0vqEuicqybO93skyE9)

---

Now let's get into something a bit more experimental...

I've devised a simple example of how one might attempt to scrape the contents of a webpage and summarize whatever is found there. Because any given webpage might have a lot of text, **this script will possibly generate many requests to ChatGPT depending on the webpage. You have been warned.**

```
python3 autogpt_test.py <url>
```

[![asciicast](https://asciinema.org/a/zwZD5PQVR2BQg6mdZmf4rxT8m.svg)](https://asciinema.org/a/zwZD5PQVR2BQg6mdZmf4rxT8m)

