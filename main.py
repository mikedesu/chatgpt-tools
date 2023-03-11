import os
import openai
import sys
from datetime import datetime
from rich import print

dan_prompt = ''

def get_dan_prompt():
    global dan_prompt
    with open('dan.txt', 'r') as f:
        dan_prompt = f.read()


def main():
    t0 = datetime.now()
    openai.organization = 'evildojo'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    get_dan_prompt()
    my_model = 'gpt-3.5-turbo'
    messages = []
    message = {'role': 'system', 'content': dan_prompt}
    #message = {'role': 'user', 'content': my_prompt}
    messages.append(message)
    test_obj = openai.ChatCompletion.create(
        model=my_model,
        messages=messages
    )
    response = test_obj["choices"][0]["message"]["content"]
    message = {'role': 'assistant', 'content': response}
    messages.append(message)
    print(response)
    t1 = datetime.now()
    t_diff = t1-t0
    print(t_diff)
    input_msg = input("Enter your message: ")
    while input_msg != 'exit':
        message = {'role': 'user', 'content': input_msg}
        messages.append(message)
        t0 = datetime.now()
        test_obj = openai.ChatCompletion.create(
            model=my_model,
            messages=messages
        )
        response = test_obj["choices"][0]["message"]["content"]
        message = {'role': 'assistant', 'content': response}
        messages.append(message)
        print(response)
        t1 = datetime.now()
        t_diff = t1-t0
        print(t_diff)
        input_msg = input("Enter your message: ")


if __name__ == '__main__':
    main()

