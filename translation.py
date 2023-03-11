import os
import openai
import sys
from datetime import datetime
from rich import print
from time import sleep
import json

prompt = 'You are my translation assistant. I will ask you to translate texts from various languages, in particular Japanese, into English.'


def main():
    t0 = datetime.now()
    openai.organization = 'evildojo'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    my_model = 'gpt-3.5-turbo'
    messages = []
    message = {'role': 'system', 'content': prompt}
    messages.append(message)
    test_obj = openai.ChatCompletion.create(
        model=my_model,
        messages=messages
    )
    response = test_obj["choices"][0]["message"]["content"]
    message = {'role': 'assistant', 'content': response}
    messages.append(message)
    print("[bold green]ChatGPT:[/bold green]",response)
    t1 = datetime.now()
    t_diff = t1-t0
    print("Response time: ",t_diff)

    print("[bold green]You:[/bold green] ", end='')
    input_msg = input()
    while input_msg != 'exit' and input_msg != 'quit':
        message = {'role': 'user', 'content': input_msg}
        messages.append(message)
        t0 = datetime.now()

        test_obj = None

        while test_obj is None:
            try:
                test_obj = openai.ChatCompletion.create(
                    model=my_model,
                    messages=messages
                )
            except Exception as e:
                print("[bold red]Error[/bold red]: ",e)
                print("[bold purple]Info[/bold purple]: sleeping for 60 seconds...")
                # chances are the error was a rate limiting issue
                # so we'll just wait a few seconds and try again
                test_obj = None
                sleep(60)

        response = test_obj["choices"][0]["message"]["content"]
        message = {'role': 'assistant', 'content': response}
        messages.append(message)
        print("[bold green]ChatGPT:[/bold green]",response)
        t1 = datetime.now()
        t_diff = t1-t0
        print(t_diff)

        filename_index = 0
        filename = f"chatlog{filename_index}.json"
        # check to see if filename exists
        while os.path.exists(filename):
            filename_index += 1
            filename = f"chatlog{filename_index}.json"
        # write messages to file
        with open(filename, "w") as f:
            f.write(json.dumps(messages, indent=4))

        print("[bold green]You:[/bold green] ", end='')
        input_msg = input()



if __name__ == '__main__':
    main()

