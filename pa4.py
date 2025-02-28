import os
import sys
import json
import rich
from time import sleep
from openai import OpenAI
from datetime import datetime


response_times = []


def calculate_average_response_time():
    if len(response_times) == 0:
        return 0
    return sum(response_times) / len(response_times)


def initialize_prompt(f):
    with open(f, "r") as r:
        return "".join(r.read().splitlines())


def create_chat_message(role, content):
    return {"role": role, "content": content}


def send_message(c, m, msgs):
    t0 = datetime.now()
    while True:
        try:
            r = c.chat.completions.create(model=m, messages=msgs)
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
            if not r.choices:
                raise Exception("No choices in result")
            if not r.choices[0].message.content:
                raise Exception("Empty message content")
            return r.choices[0].message.content
        except Exception as e:
            rich.print(f"Error: {e}")
            for i in range(5):
                rich.print(f"Info: Sleeping for {5-i} seconds...")
                sleep(1)


def log_chat(m, d="chatlogs"):
    os.makedirs(d, exist_ok=True)
    i = 0
    f = os.path.join(d, f"chatlog{i}.json")
    while os.path.exists(f):
        i += 1
        f = os.path.join(d, f"chatlog{i}.json")
    with open(f, "w") as o:
        print("Info: writing chatlog to", f)
        o.write(json.dumps(m, indent=4))


def print_token_count(m):
    t = sum(len(msg["content"]) for msg in m)
    rich.print(f"Info: current tokens used: {t}")


def print_num_messages(messages):
    rich.print("[bold purple]Info[/bold purple]: current messages:", len(messages))


def print_response(model, response):
    rich.print(f"[bold green]{model}[/bold green]:", response, "\n")


def main_loop(c, model, messages):
    response = send_message(c, model, messages)
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
        one_nl = False
        double_nl = False
        while double_nl == False:
            if input_msg == "":
                one_nl = True
            lines.append(input_msg)
            input_msg = input()
            if input_msg == "" and one_nl == True:
                double_nl = True
        input_msg = "\n".join(lines).strip()
        rich.print("--------------------")
        messages.append(create_chat_message("user", input_msg))
        response = send_message(c, model, messages)
        messages.append(create_chat_message("assistant", response))
        print_response(model, response)
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


def init_xai_client():
    return OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )


def init_openai_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG"),
    )


def init_client(provider):
    if provider == "xai":
        return init_xai_client()
    elif provider == "openai":
        return init_openai_client()


def main():
    p = "xai"
    m = []
    c = init_client(p)
    a = sys.argv
    m = [create_chat_message("system", initialize_prompt(a[2]))]
    try:
        main_loop(c, a[1], m)
        # main_loop(c, m[0]["content"], a[1], m)
    except KeyboardInterrupt:
        print("\nExiting...")
        log_chat(m)
    print_avg_response_time()


if __name__ == "__main__":
    main()
