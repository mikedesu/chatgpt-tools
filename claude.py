import anthropic
import rich
import sys
from rich.markdown import Markdown
import json
import os


def print_hr():
    """Prints a horizontal rule."""
    rich.print(Markdown("--------------------"))


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


def main():
    client = anthropic.Anthropic()
    messages = []
    model = "claude-3-5-sonnet-20241022"
    # model = "claude-3-7-sonnet-20250219"
    prompt = ""
    prompt_filename = sys.argv[1] if len(sys.argv) > 1 else "prompt.txt"
    with open(prompt_filename, "r") as f:
        prompt = f.read()
    max_tokens = 1024
    try:
        while True:
            rich.print("[bold green]You:[/bold green] ", end="")
            input_msg_list = []
            input_msg = input().strip()
            while input_msg != "done" and input_msg != "d":
                input_msg_list.append(input_msg)
                input_msg = input().strip()
            input_msg = "\n".join(input_msg_list)
            if input_msg == "exit" or input_msg == "e":
                break
            messages.append(
                {
                    "role": "user",
                    "content": input_msg,
                }
            )
            print_hr()
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=prompt,
                messages=messages,
            )
            response_content = response.content[0].text
            rich.print(f"[bold green]{model}[/bold green]: {response_content}")
            response_message = {
                "role": "assistant",
                "content": response_content,
            }
            messages.append(response_message)
    except KeyboardInterrupt:
        print_hr()
        log_chat("claude-3-5-sonnet", messages)
        rich.print("[bold red]Exiting...[/bold red]")


if __name__ == "__main__":
    main()
