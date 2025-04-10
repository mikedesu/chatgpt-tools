from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in the root directory",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "load_file",
            "description": "Load the contents of a file into our file memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the file to get",
                    },
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_line_count",
            "description": "Get the number of lines in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the file to get",
                    },
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_line_in_file",
            "description": "Get a specific line in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the file to get",
                    },
                    "line": {
                        "type": "integer",
                        "description": "The line number to get",
                    },
                },
                "required": ["name", "line"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_part_of_file",
            "description": "Get a specific part of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the file to get",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "The starting line number to get",
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "The ending line number to get",
                    },
                },
                "required": ["name", "start_line", "end_line"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_contents",
            "description": "Get the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the file to get",
                    },
                },
                "required": ["name"],
            },
        },
    },
]


root_dir = "/home/darkmage/src/mikedesu/c/raylib-rpg-c/src"

messages = []

file_memory = {}


def list_files():
    proj_dir = "/home/darkmage/src/mikedesu/c/raylib-rpg-c/src"
    files = []
    # only add files in the dir, do not recursively add files in subdirs
    # i said DO NOT RECURSIVELY ADD FILES IN SUBDIRS
    for root, dirs, filenames in os.walk(proj_dir):
        for filename in filenames:
            if filename.endswith(".c") or filename.endswith(".h"):
                files.append(filename)
            # also add the makefile
            if filename == "Makefile":
                files.append(filename)
            # also add any .ini files or .txt files
            if filename.endswith(".ini") or filename.endswith(".txt"):
                files.append(filename)
        break
    return " ".join(files)


def load_file(name):
    global file_memory
    file_path = os.path.join(root_dir, name)
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist."
    with open(file_path, "r") as f:
        contents = f.read()
    # store the contents in file memory
    file_memory[name] = contents
    return contents


def get_file_line_count(name):
    global file_memory
    if name not in file_memory:
        return f"File {name} not loaded."
    lines = file_memory[name].splitlines()
    return len(lines)


def get_line_in_file(name, line):
    global file_memory
    if name not in file_memory:
        return f"File {name} not loaded."
    lines = file_memory[name].splitlines()
    if line < 0 or line >= len(lines):
        return f"Line {line} out of range for file {name}."
    return lines[line]


def get_part_of_file(name, start_line, end_line):
    global file_memory
    if name not in file_memory:
        return f"File {name} not loaded."
    lines = file_memory[name].splitlines()
    if start_line < 0 or end_line >= len(lines):
        return f"Line {start_line} to {end_line} out of range for file {name}."
    return lines[start_line:end_line]


def get_file_contents(name):
    global file_memory
    if name not in file_memory:
        return f"File {name} not loaded."
    return file_memory[name]


def run_function(func_name, func_args):
    if func_name == "list_files":
        return list_files()
    elif func_name == "load_file":
        return load_file(func_args["path"])


messages.append(
    {
        "role": "user",
        "content": "What files are available in the game's source directory?",
    }
)

response = client.chat.completions.create(
    model="gemini-2.0-flash", messages=messages, tools=tools, tool_choice="auto"
)


resp_msg = response.choices[0].message

print(f"Response: {resp_msg}")

content = resp_msg.content
tool_calls = resp_msg.tool_calls

# we need to check if the response contains a function call
if tool_calls:
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        result = run_function(func_name, func_args)
        # print(f"Function result: {result}")
        messages.append(
            {
                "role": "assistant",
                "content": result,
            }
        )

    # now send it back to LLM
    response = client.chat.completions.create(
        model="gemini-2.0-flash", messages=messages, tools=tools
    )

    print(f"Model response: {response.choices[0].message.content}")

    messages.append(
        {
            "role": "user",
            "content": "Excellent. Which file contains the main function?",
        }
    )

    response = client.chat.completions.create(
        model="gemini-2.0-flash", messages=messages, tools=tools, tool_choice="auto"
    )

    resp_msg = response.choices[0].message

    print(f"Response: {resp_msg}")

    content = resp_msg.content
    tool_calls = resp_msg.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            result = run_function(func_name, func_args)
            # print(f"Function result: {result}")
            messages.append(
                {
                    "role": "assistant",
                    "content": result,
                }
            )

        # now send it back to LLM
        response = client.chat.completions.create(
            model="gemini-2.0-flash", messages=messages, tools=tools
        )

        print(f"Model response: {response.choices[0].message.content}")
