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
            "description": "List the files in the source code directory",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file",
            "description": "Get the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to get",
                    },
                },
                "required": ["path"],
            },
        },
    },
]


def list_files():
    proj_dir = "/home/darkmage/src/mikedesu/c/raylib-rpg-c/src"
    files = []
    # only add files in the dir, do not recursively add files in subdirs
    # i said DO NOT RECURSIVELY ADD FILES IN SUBDIRS
    for root, dirs, filenames in os.walk(proj_dir):
        for filename in filenames:
            if filename.endswith(".c") or filename.endswith(".h"):
                files.append(filename)
        break
    return " ".join(files)


def get_file(path):
    proj_dir = "/home/darkmage/src/mikedesu/c/raylib-rpg-c/src"
    file_path = os.path.join(proj_dir, path)
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist."
    with open(file_path, "r") as f:
        contents = f.read()
    return contents


def run_function(func_name, func_args):
    if func_name == "list_files":
        return list_files()
    elif func_name == "get_file":
        return get_file(func_args["path"])


messages = [
    {
        "role": "user",
        "content": "What files are available in the game's source directory?",
    }
]
response = client.chat.completions.create(
    model="gemini-2.0-flash", messages=messages, tools=tools, tool_choice="auto"
)


resp_msg = response.choices[0].message

print(f"Response: {resp_msg}")

content = resp_msg.content
tool_calls = resp_msg.tool_calls

messages.append(
    {
        "role": resp_msg.role,
        "content": "" if content is None else content,
        "tool_calls": "" if tool_calls is None else tool_calls,
    }
)

# we need to check if the response contains a function call
if tool_calls:
    tool_call_results = []
    for i in range(len(tool_calls)):
        tool_call = tool_calls[i]
        print(f"Tool call: {tool_call}")
        tool_call_function = tool_call.function
        func_args = tool_call_function.arguments
        func_name = tool_call_function.name
        print(f"Function name: {func_name}")
        print(f"Function arguments: {func_args}")
        # Call the function with the arguments
        result = run_function(func_name, func_args)
        print(f"Function result: {result}")
        # Add the result to the tool call results
        tool_call_result = {
            "name": func_name,
            "response": {
                "content": result,
            },
        }
        tool_call_results.append(result)

    # tool_call_results = " ".join(tool_call_results)
    messages.append(
        {
            "role": "assistant",
            "content": f"The results from the function calls are: {tool_call_results}",
            "tool_calls": tool_call_results,
        }
    )

    # send the results back to the model
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    resp_msg = response.choices[0].message
    content = resp_msg.content
    tool_calls = resp_msg.tool_calls

    if content:
        print(f"Response: {content}")
    if tool_calls:
        print(f"Tool calls: {tool_calls}")
