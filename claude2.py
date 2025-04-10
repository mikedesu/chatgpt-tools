import anthropic, rich, sys, json, os
from rich.markdown import Markdown


def print_hr():
    rich.print(Markdown("-" * 20))


def log_chat(provider, msgs, log_dir="chatlogs"):
    os.makedirs(log_dir, exist_ok=True)
    i = 0
    while os.path.exists(f := os.path.join(log_dir, f"chatlog-{provider}-{i}.json")):
        i += 1
    rich.print(f"Info: writing to {f}")
    json.dump(msgs, open(f, "w"), indent=4)


def main():
    c = anthropic.Anthropic()
    msgs = []
    model = "claude-3-5-sonnet-20241022"
    max_tokens = 1024
    with open(sys.argv[1] if len(sys.argv) > 1 else "prompt.txt") as f:
        sys_prompt = f.read()
    try:
        while True:
            rich.print("[bold green]You[/bold green]: ", end="")
            lines = []
            while (line := input().strip()) not in ["done", "d"]:
                lines.append(line)
            msg = "\n".join(lines)
            if msg in ["exit", "e"]:
                break
            msgs.append({"role": "user", "content": msg})
            print_hr()
            resp = c.messages.create(
                model=model, max_tokens=max_tokens, system=sys_prompt, messages=msgs
            )
            resp_txt = resp.content[0].text
            rich.print(f"[bold green]{model}[/bold green]: {resp_txt}")
            msgs.append({"role": "assistant", "content": resp_txt})
    except KeyboardInterrupt:
        print_hr()
        log_chat(model, msgs)
        rich.print("Exiting...")


if __name__ == "__main__":
    main()
