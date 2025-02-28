import os, sys, json, rich
from time import sleep
from openai import OpenAI
from datetime import datetime

r = []


def a():
    return sum(r) / len(r) if r else 0


def i(f):
    with open(f) as h:
        return "".join(h.read().splitlines())


def cc(r, c):
    return {"role": r, "content": c}


def s(c, m, msgs):
    t0 = datetime.now()
    while 1:
        try:
            h = c.chat.completions.create(model=m, messages=msgs)
            t1 = datetime.now()
            r.append((t1 - t0).total_seconds())
            if not h.choices:
                raise Exception("No choices in result")
            if not h.choices[0].message.content:
                raise Exception("Empty message content")
            return h.choices[0].message.content
        except Exception as e:
            rich.print(f"Error: {e}")
            for i in range(5):
                rich.print(f"Info: Sleeping for {5-i} seconds...")
                sleep(1)


def l(m, d="chatlogs"):
    os.makedirs(d, exist_ok=True)
    i = 0
    f = os.path.join(d, f"chatlog{i}.json")
    while os.path.exists(f):
        i += 1
        f = os.path.join(d, f"chatlog{i}.json")
    with open(f, "w") as o:
        print("Info: writing chatlog to", f)
        o.write(json.dumps(m, indent=4))


def p(m, r):
    rich.print(f"[bold green]{m}[/bold green]:", r, "\n")


def m(c, m, msgs):
    r = s(c, m, msgs)
    msgs.append(cc("assistant", r))
    p(m, r)
    while 1:
        lines = []
        rich.print("You: ", end="")
        try:
            i = input()
        except EOFError:
            break
        one_nl = False
        double_nl = False
        while not double_nl:
            if i == "":
                one_nl = True
            lines.append(i)
            i = input()
            if i == "" and one_nl:
                double_nl = True
        i = "\n".join(lines).strip()
        rich.print("--------------------")
        msgs.append(cc("user", i))
        r = s(c, m, msgs)
        msgs.append(cc("assistant", r))
        p(m, r)
    l(msgs)


def u():
    if len(sys.argv) != 3:
        print("Usage: python3 pa.py <model> <prompt_filepath>")
        sys.exit(1)


def v():
    rich.print(
        f"[bold purple]Info:[/bold purple] average response time is {a():.2f} seconds"
    )


def x():
    return OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")


def o():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORG")
    )


def w(p):
    return x() if p == "xai" else o()


def main():
    p = "xai"
    msgs = []
    c = w(p)
    a = sys.argv
    msgs = [cc("system", i(a[2]))]
    try:
        m(c, a[1], msgs)
    except KeyboardInterrupt:
        print("\nExiting...")
        l(msgs)
    v()


if __name__ == "__main__":
    main()
