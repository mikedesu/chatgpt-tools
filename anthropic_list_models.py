import anthropic


def main():
    client = anthropic.Anthropic()
    out = client.models.list(limit=20)
    for model in out:
        print(model.id)


if __name__ == "__main__":
    main()
