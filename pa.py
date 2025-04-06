import os
import sys
import json
import rich
import tiktoken
from openai import OpenAI
from datetime import datetime
from time import sleep
from rich.console import Console

from rich.markdown import Markdown
from typing import Any

response_times = []

token_checker = tiktoken.encoding_for_model("gpt-4o")

total_tokens_this_session = 0


def calculate_average_response_time(response_times: list) -> float:
    if not response_times:
        return 0.0
    return sum(response_times) / len(response_times)


def initialize_prompt(filename: str) -> str:
    """Reads and flattens a prompt file into a single line."""
    with open(filename, "r") as f:
        return f.read().replace("\n", " ").strip()


# def create_chat_message(role, content):
#    return {"role": role, "content": content}


def create_chat_message(role: str, content: str) -> dict:
    return {"role": role, "content": content}


def send_message(client, model, messages):
    t0 = datetime.now()
    while True:
        try:
            result = client.chat.completions.create(
                model=model, messages=messages, stream=False
            )
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
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

            # we never want to see this...
            # if we do, we need to
            # 1. prune off the most recent message we added to the messages list
            # 2. prune off the most recent message we received from the assistant
            # 3. ask it to summarize everything up to this point
            # 4. clear the messages list and add the system prompt and summary
            # if "maximum context length" in str(e):
            #    rich.print(
            #        "[bold red]Error[/bold red]: maximum context length exceeded, "
            #        "please shorten your prompt or conversation history."
            #    )
            #    break

            sleep_time = 5
            for i in range(sleep_time):
                rich.print(
                    f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds..."
                )
                sleep(1)


def log_chat(provider, messages, chatlog_dir="chatlogs"):
    os.makedirs(chatlog_dir, exist_ok=True)  # Create dir if it doesn't  exist
    index = 0
    while os.path.exists(
        filename := os.path.join(chatlog_dir, f"chatlog-{provider}-{index}.json")
    ):
        index += 1
    with open(filename, "w") as f:
        rich.print(f"[bold purple]Info[/bold purple]: writing chatlog to {filename}")
        json.dump(messages, f, indent=4)


# def print_token_count(messages):
#    token_count = 0
#    for msg in messages:
#        token_count += len(msg["content"])
#    rich.print("[bold purple]Info[/bold purple]: current tokens used:", token_count)


def print_token_count(messages: list) -> None:
    """Prints total token count from message content."""
    token_count = sum(len(m["content"]) for m in messages)
    rich.print(f"[bold purple]Info[bold purple]: current tokens used: {token_count}")


# def print_num_messages(messages):
#    rich.print("[bold purple]Info[/bold purple]: current messages:", len(messages))


def print_num_messages(messages: list) -> None:
    """Prints the count of messages."""
    rich.print(f"[bold purple]Info[bold purple]: current messages: {len(messages)}")


# def print_response(model, response):
#    rich.print(f"[bold green]{model}[/bold green]:", response, "\n")


def print_response(model: str, response: Any) -> None:
    """Pretty-prints model responses using rich formatting."""
    response += "\n\n-------------------\n"
    # mkdn = Markdown(response)
    # rich.print(f"[bold green]{model}[/bold green]:", mkdn, "\n")
    rich.print(f"[bold green]{model}[/bold green]:", response, "\n")
    # Console().print(f"{model}:", response, "\n")


def main_loop(provider, client, model, messages):
    global total_tokens_this_session
    # prompt = messages[-1]["content"]
    response = send_message(client, model, messages)
    messages.append(create_chat_message("assistant", response))
    print_response(model, response)
    while True:
        lines = []
        rich.print("[bold green]You[/bold green]: ", end="")
        input_msg = ""
        try:
            input_msg = input()
        except EOFError:
            break
        if input_msg in ("exit", "quit"):
            break
        if input_msg in ("file", "f"):
            # read from a file
            rich.print("[bold green]Filepath[/bold green]: ", end="")
            input_msg = input().strip()
            with open(input_msg, "r") as f:
                lines = f.readlines()
                input_msg = "".join(lines)
                input_msg = input_msg.strip()
        else:
            one_newline_entered = False
            double_newline_entered = False
            while double_newline_entered == False:
                if input_msg == "":
                    one_newline_entered = True
                else:
                    one_newline_entered = False
                lines.append(input_msg)
                input_msg = input()
                if input_msg == "" and one_newline_entered == True:
                    double_newline_entered = True
            input_msg = "\n".join(lines)
            input_msg = input_msg.strip()
            if input_msg in ("exit", "quit"):
                break
        tokens = token_checker.encode(input_msg)
        token_count = len(tokens)
        rich.print(
            f"[bold purple]Info[/bold purple]: estimated tokens send: {token_count}"
        )
        total_tokens_this_session += token_count
        markdown_hr = Markdown("--------------------")
        rich.print(markdown_hr)
        messages.append(create_chat_message("user", input_msg))
        response = send_message(client, model, messages)
        # print estimated token count for response
        tokens = token_checker.encode(response)
        token_count = len(tokens)
        rich.print(
            f"[bold purple]Info[/bold purple]: estimated tokens recv: {token_count}"
        )
        total_tokens_this_session += token_count
        rich.print(
            f"[bold purple]Info[/bold purple]: total tokens used....: {total_tokens_this_session}"
        )
        print()
        messages.append(create_chat_message("assistant", response))
        if "summarize" in input_msg:
            # summarize the conversation
            # we want to keep the first 2 messages and the last 2 messages
            # and delete the rest
            updated_messages = messages[:2] + messages[-2:]
            messages = updated_messages
            rich.print(f"[bold purple]Info[/bold purple]: {messages}")
            # rich.print("--------------------")
            rich.print(markdown_hr)
        print_response(model, response)
    log_chat(provider, messages)


def print_usage():
    print("Usage: python3 pa.py <provider> <model> <prompt_filepath>")


def check_usage():
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)


def print_avg_response_time():
    secs = calculate_average_response_time(response_times)
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
    elif provider == "llama":
        return OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-required")
    elif provider == "deepseek":
        return OpenAI(
            base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY")
        )


def main():
    check_usage()
    provider = sys.argv[1]
    messages = []
    model = sys.argv[2]
    client = init_client(provider)
    prompt = initialize_prompt(sys.argv[3])
    messages = [create_chat_message("system", prompt)]
    try:
        main_loop(provider, client, model, messages)
    except KeyboardInterrupt:
        print("\nExiting...")
        log_chat(provider, messages)
    print_avg_response_time()


if __name__ == "__main__":
    main()
