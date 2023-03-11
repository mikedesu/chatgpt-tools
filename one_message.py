import os
import openai
import sys
from datetime import datetime



def usage():
    print("usage:")
    print()
    print("python3 main.py <prompt>")
    sys.exit(-1)


def handle_usage():
    if len(sys.argv)!=2:
        usage()


def main():
    t0 = datetime.now()
    openai.organization = 'evildojo'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    handle_usage()

    my_prompt = sys.argv[1]
    my_model = 'gpt-3.5-turbo'

    messages = []
    message = {'role': 'user', 'content': my_prompt}
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


if __name__ == '__main__':
    main()

