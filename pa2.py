import os
import openai
from openai import OpenAI
import sys
import json
import rich
import signal
from datetime import datetime
from time import sleep


# provider = "openai"
provider = "xai"
model = None
prompt = None

response_times = []


def calculate_average_response_time():
    if len(response_times) == 0:
        return 0
    return sum(response_times) / len(response_times)


def initialize_prompt(filename):
    with open(filename, "r") as f:
        prompt = f.read()
    prompt = "".join(prompt.splitlines())
    return prompt


def create_chat_message(role, content):
    return {"role": role, "content": content}


def send_message(client, model, messages):
    t0 = datetime.now()
    while True:
        try:
            result = client.chat.completions.create(model=model, messages=messages)
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
            # print("[bold purple]Info[/bold purple]: message sent in", tdiff.total_seconds(), "seconds")
            # make sure result.choices is not empty
            if len(result.choices) == 0:
                raise Exception("result.choices is empty")
            # make sure message is not empty
            if result.choices[0].message.content == "":
                raise Exception("result.choices[0].message.content is empty")
            # return the response
            return result.choices[0].message.content
        except Exception as e:
            rich.print("[bold red]Error[/bold red]: ", e)
            sleep_time = 5
            for i in range(sleep_time):
                rich.print(
                    f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds..."
                )
                sleep(1)


def log_chat(messages, chatlog_dir="chatlogs"):
    index = 0
    # verify directory exists
    if not os.path.exists(chatlog_dir):
        os.makedirs(chatlog_dir)
    filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    while os.path.exists(filename):
        index += 1
        filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    with open(filename, "w") as f:
        rich.print("[bold purple]Info[/bold purple]: writing chatlog to", filename)
        f.write(json.dumps(messages, indent=4))


def print_token_count(messages):
    token_count = 0
    for msg in messages:
        token_count += len(msg["content"])
    rich.print("[bold purple]Info[/bold purple]: current tokens used:", token_count)


def print_num_messages(messages):
    rich.print("[bold purple]Info[/bold purple]: current messages:", len(messages))


def print_response(model, response):
    rich.print(f"[bold green]{model}[/bold green]:", response, "\n")


def main_loop(client, model, messages):
    response = send_message(client, model, messages)
    messages.append(create_chat_message("assistant", response))
    print_response(model, response)
    while True:
        lines = []
        rich.print("[bold]You[/bold]: ", end="")
        input_msg = ""
        try:
            input_msg = input()
        except EOFError:
            break
        if input_msg in ("exit", "quit"):
            break
        one_newline_entered = False
        double_newline_entered = False
        while double_newline_entered == False:
            if input_msg == "":
                one_newline_entered = True
            lines.append(input_msg)
            input_msg = input()
            if input_msg == "" and one_newline_entered == True:
                double_newline_entered = True
        input_msg = "\n".join(lines).strip()
        rich.print("--------------------")
        if input_msg in ("exit", "quit"):
            break
        if input_msg in ("clear", "cls", "c"):
            messages.clear()
            messages.append(create_chat_message("system", prompt))
            continue
        if input_msg in ("tokens", "t"):
            print_token_count(messages)
            continue
        if input_msg in ("write", "w"):
            filename = input("filename: ")
            with open(filename, "w") as f:
                f.write(messages[-1]["content"])
            continue
        messages.append(create_chat_message("user", input_msg))
        response = send_message(client, model, messages)
        messages.append(create_chat_message("assistant", response))
        print_response(model, response)
        # print_token_count(messages)
        # print_num_messages(messages)
        # print_avg_response_time()
    log_chat(messages)


def check_usage():
    if len(sys.argv) != 3:
        print("Usage: python3 pa.py <model> <prompt_filepath>")
        sys.exit(1)


def print_avg_response_time():
    secs = calculate_average_response_time()
    outstr = (
        f"[bold purple]Info[/bold purple]: average response time is {secs:.2f} seconds"
    )
    rich.print(outstr)


def init_client(provider):
    if provider == "xai":
        return OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1",
        )
    elif provider == "openai":
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG"),
        )


def main():
    p = "xai"
    m = []
    c = init_client(p)
    a = sys.argv
    m = [create_chat_message("system", initialize_prompt(a[2]))]
    try:
        main_loop(c, a[1], m)
    except KeyboardInterrupt:
        print("\nExiting...")
        log_chat(m)
    print_avg_response_time()


if __name__ == "__main__":
    main()
