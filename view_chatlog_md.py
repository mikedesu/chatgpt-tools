import json
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 view_chatlog.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        messages = json.load(f)
    for i in range(2, len(messages)):
        message = messages[i]
        # keys are 'role' and 'content'
        print("> **" + message['role'] + '**: ' + message['content'])
        if i < len(messages) - 1:
            print("-----")

if __name__ == '__main__':
    main()

