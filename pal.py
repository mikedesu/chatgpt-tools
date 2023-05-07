# this version was refactored by GPT-4 on 03-24-2023
import os
import openai
import sys
import json
import rich
from datetime import datetime
from time import sleep


response_times = []


def calculate_average_response_time():
    if len(response_times) == 0:
        return 0
    return sum(response_times) / len(response_times)


def initialize_prompt(filename):
    with open(filename, 'r') as f:
        prompt = f.read()
    prompt = "".join(prompt.splitlines())
    return prompt


def initialize_openai():
    openai.organization = 'evildojo'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    #if sys.argv[2] == 'gpt-3.5-turbo-0301':
    if 'gpt-3' in sys.argv[2] or 'gpt3' in sys.argv[2]:
        return 'gpt-3.5-turbo'
    if 'gpt-4' in sys.argv[2] or 'gpt4' in sys.argv[2]:
        return 'gpt-4'
    # error out 
    #print("[bold red]Error[/bold red]: invalid model")
    print("Error: invalid model")
    sys.exit(1)


def create_chat_message(role, content):
    return {'role': role, 'content': content}


def send_message(model, messages):
    t0 = datetime.now()
    while True:
        try:
            result = openai.ChatCompletion.create(model=model, messages=messages)
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
            #print("[bold purple]Info[/bold purple]: message sent in", tdiff.total_seconds(), "seconds")
            return result["choices"][0]["message"]["content"]
        except InvalidRequestError as e:
            print("[bold red]Error[/bold red]: ", e)
            sleep_time = 30
            for i in range(sleep_time):
                rich.print(f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds...")
                sleep(1)
        except Exception as e:
            print("[bold red]Error[/bold red]: ", e)
            sleep_time = 10
            for i in range(sleep_time):
                rich.print(f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds...")
                sleep(1)


def log_chat(messages, chatlog_dir="chatlogs"):
    index = 0
    filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    while os.path.exists(filename):
        index += 1
        filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    with open(filename, "w") as f:
        f.write(json.dumps(messages, indent=4))


def print_token_count(messages):
    token_count = 0
    for msg in messages:
        token_count += len(msg['content'])
    rich.print("[bold purple]Info[/bold purple]: current tokens used:", token_count)
        

def print_num_messages(messages):
    rich.print("[bold purple]Info[/bold purple]: current messages:", len(messages))


def print_response(response):
    print("> **ChatGPT**:", response)


def main_loop(model, messages):
    response = send_message(model, messages)
    messages.append(create_chat_message('assistant', response))
    print_response(response)
    while True:
        print("> **You**: ", end='')
        input_msg = input()
        
        if input_msg in ('exit', 'quit'):
            break

        if input_msg in ('clear', 'cls', 'c'):
            messages.clear()
            messages.append(create_chat_message('system', prompt))
            continue

        if input_msg in ('tokens', 't'):
            print_token_count(messages)
            continue
        
        if input_msg in ('write', 'w'):
            filename = input("filename: ")
            with open(filename, 'w') as f:
                f.write(messages[-1]['content'])
            continue

        if input_msg in ('multiline', 'm'):
            lines = []
            #print("[bold green]You:[/bold green] ", end='')
            print("> **You**: ", end='')
            input_msg = input()
            while input_msg != 'end':
                lines.append(input_msg)
                input_msg = input()
            input_msg = '\n'.join(lines)
        
        messages.append(create_chat_message('user', input_msg))
        response = send_message(model, messages)
        messages.append(create_chat_message('assistant', response))
        
        print_response(response)
        #print_token_count(messages)
        #print_num_messages(messages)
        #print_avg_response_time()
        log_chat(messages)


def check_usage():
    if len(sys.argv) != 3:
        print("Usage: python assistant.py <prompt_filename> <model>")
        sys.exit(1)


def print_avg_response_time():
    secs = calculate_average_response_time()
    outstr = f"[bold purple]Info[/bold purple]: average response time is {secs:.2f} seconds"
    rich.print(outstr)


def main():
    # check usage
    check_usage()
    prompt_filename = sys.argv[1]
    prompt = initialize_prompt(prompt_filename)
    model = initialize_openai()
    messages = [create_chat_message('system', prompt)]

    try:
        main_loop(model, messages)
    except KeyboardInterrupt:
        rich.print("-"*20)
        rich.print("Exiting...")
    
    print_avg_response_time()


if __name__ == '__main__':
    main()

