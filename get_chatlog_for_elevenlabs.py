import json
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python view_chatlog.py <filename>")
        return
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        messages = json.load(f)
    for i in range(2, len(messages)):
        message = messages[i]
        # keys are 'role' and 'content'
        content = message['content']
        # if there are any newlines, replace them with spaces
        content = content.replace('\n', ' ')
        # remove any backticks
        content = content.replace('`', '')
        # replace any double spaces with single spaces
        content = content.replace('  ', ' ')
        print(content)
        print()


if __name__ == '__main__':
    main()

