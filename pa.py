import os
import sys
import json
import rich
import tiktoken
from openai import OpenAI
from datetime import datetime
from time import sleep
from rich.markdown import Markdown
from typing import Any
from datetime import timedelta

response_times = []
token_checker = tiktoken.encoding_for_model("gpt-4o")
total_tokens_this_session = 0

MODEL_CONTEXT = {
    # OpenAI
    "gpt-4o": 128000,
    "gpt-4-turbo": 128000,
    "gpt-3.5-turbo": 16000,
    # xAI
    "grok-2-latest": 128000,
    # Deepseek
    "deepseek-chat": 128000,
    # Google (conservative)
    "gemini-1.5": 32000,
    # Local
    "llama3-8b": 8000,
}


def calculate_average_response_time(response_times: list) -> float:
    if not response_times:
        return 0.0
    return sum(response_times) / len(response_times)


def initialize_prompt(filename: str) -> str:
    """Reads and flattens a prompt file into a single line."""
    with open(filename, "r") as f:
        return f.read().replace("\n", " ").strip()


def create_chat_message(role: str, content: str) -> dict:
    return {"role": role, "content": content}


def send_message(client, model, messages):
    t0 = datetime.now()
    while True:
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            print()
            print("-------------------")
            print()
            rich.print(f"[bold green]{model}[/bold green]: ", end="", flush=True)
            content = ""
            timeout_seconds = 120
            timeout = timedelta(seconds=timeout_seconds)
            start_time = datetime.now()
            for chunk in stream:
                if datetime.now() - start_time > timeout:
                    raise TimeoutError("Stream response timed out")
                if not chunk.choices:  # Guard against empty choices
                    continue
                delta = chunk.choices[0].delta  # Safe after empty check
                if delta and delta.content:  # Validate delta exists
                    print(delta.content, end="", flush=True)
                    content += delta.content
            print()
            print("-------------------")
            print()
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
            return content
        except Exception as e:
            rich.print("[bold red]Error[/bold red]: ", e)
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


def print_token_count(messages: list) -> None:
    """Prints actual token count from message content."""
    tokens = sum(len(token_checker.encode(m["content"])) for m in messages)
    rich.print(f"[bold purple]Info[/bold purple]: current tokens used: {tokens}")


def print_num_messages(messages: list) -> None:
    """Prints the count of messages."""
    rich.print(f"[bold purple]Info[bold purple]: current messages: {len(messages)}")


def print_response(model: str, response: Any) -> None:
    """Pretty-prints model responses using rich formatting."""
    response += "\n\n-------------------\n"
    rich.print(f"[bold green]{model}[/bold green]:", response, "\n")


def main_loop(provider, client, model, messages):
    global total_tokens_this_session
    response_content = send_message(client, model, messages)
    messages.append(create_chat_message("assistant", response_content))
    while True:
        lines = []
        rich.print("[bold green]You[/bold green]: ", end="")
        input_msg = ""
        try:
            input_msg = input()
            if input_msg.startswith("/"):
                handle_command(client, model, input_msg, messages)  # New function
                continue
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
        response_content = send_message(client, model, messages)
        # print estimated token count for response
        if response_content:
            tokens = token_checker.encode(response_content)
            token_count = len(tokens)
            rich.print(
                f"[bold purple]Info[/bold purple]: estimated tokens recv: {token_count}"
            )
            total_tokens_this_session += token_count
            rich.print(
                f"[bold purple]Info[/bold purple]: total tokens used....: {total_tokens_this_session}"
            )
            rich.print(
                f"[bold purple]Info[/bold purple]: estimated tokens messages: {estimate_token_count(messages)}"
            )
            rich.print(
                f"[bold purple]Info[/bold purple]: estimated tokens limit...: {MODEL_CONTEXT[model]}"
            )
            # print()
            messages.append(create_chat_message("assistant", response_content))
            # print_response(model, response_content)
        else:
            rich.print("[bold yellow]Warning[/bold yellow]: no response content")
    log_chat(provider, messages)


def estimate_token_count(messages: list) -> int:
    """Estimates the token count based on the model context."""
    total_tokens = 0
    for message in messages:
        total_tokens += len(token_checker.encode(message["content"]))
    return total_tokens


def handle_command(client, model, cmd: str, messages: list) -> None:
    if cmd == "/summarize":
        summary = force_summarize(client, model, messages)
        messages[:] = [
            messages[0],
            messages[1],
            create_chat_message("assistant", summary),
        ]
    elif cmd == "/history":
        print_message_history(messages)  # New function
    elif cmd == "/reset":
        messages[:] = [
            messages[0],
            messages[1],
        ]  # Keep only system prompt and assistant response
        rich.print("History reset")


def print_message_history(messages: list) -> None:
    rich.print("\nMessage History:")
    for i, msg in enumerate(messages):
        role = msg["role"]
        x = 80
        content = (
            msg["content"][:x] + "..." if len(msg["content"]) > x else msg["content"]
        )
        rich.print(f"{i}. {role}: {content}")


def force_summarize(client, model, messages: list) -> str:
    response = send_message(
        client,
        model,
        messages
        + [
            create_chat_message(
                "user", "Summarize this conversation concisely as bullet points."
            )
        ],
    )
    return response


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


def init_client(provider) -> OpenAI:
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
    elif provider == "google":
        return OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
    # default to openai
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG"),
    )


def main():
    check_usage()
    provider = sys.argv[1]
    messages = []
    model = sys.argv[2]
    client = init_client(provider)
    prompt = initialize_prompt(sys.argv[3])
    if provider != "google":
        messages = [create_chat_message("system", prompt)]
    else:
        # Google Gemini requires the prompt to be in the first message
        messages = [create_chat_message("user", prompt)]
    try:
        main_loop(provider, client, model, messages)
    except KeyboardInterrupt:
        print("\nExiting...")
        log_chat(provider, messages)
    print_avg_response_time()


if __name__ == "__main__":
    main()
