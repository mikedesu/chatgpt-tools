import os
import string
import openai
from openai import OpenAI
import sys
import json
import rich
import signal
from datetime import datetime
from time import sleep
import pika

from rich.console import Console
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import sys
import hashlib

load_dotenv()


# rabbitmq
SLEEP_TIME = 15

model = sys.argv[1]
provider = sys.argv[2]
prompt_filename = sys.argv[3]
# initial_message = sys.argv[3]
ch1 = sys.argv[4]
ch2 = sys.argv[5]
send_initial_response = int(sys.argv[6])
voice_model_id = sys.argv[7]
connection = None
client = None  # openai or xai

elevenlabs_client = ElevenLabs()

console = Console()


if provider == "openai":
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG"),
        # api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORG")
    )
elif provider == "xai":
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )

response_times = []
messages = []


def calculate_average_response_time():
    if len(response_times) == 0:
        return 0
    return sum(response_times) / len(response_times)


def initialize_prompt(filename):
    with open(filename, "r") as f:
        prompt = f.read()
    prompt = "".join(prompt.splitlines())
    return prompt


# def initialize_openai():
#    # TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization=os.getenv('OPENAI_ORG'))'
#    # openai.organization = os.getenv('OPENAI_ORG')
#    model = sys.argv[1]
#    print("model:", model)
#    if "gpt-3.5-16k" in model or "gpt3.5-16k" in model or "gpt3.516k" in model:
#        return "gpt-3.5-turbo-16k"
#    if "gpt-3.5" in model or "gpt3.5" in model or "gpt3" in model or "gpt-3" in model:
#        return "gpt-3.5-turbo"
#    if "gpt-4" in model or "gpt4" in model:
#        return "gpt-4-1106-preview"
#    # error out
#    rich.print("[bold red]Error[/bold red]: invalid model")
#    sys.exit(1)


def create_chat_message(role, content):
    return {"role": role, "content": content}


def send_message(model, messages):
    t0 = datetime.now()
    while True:
        try:
            result = client.chat.completions.create(model=model, messages=messages)
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
            # print("[bold purple]Info[/bold purple]: message sent in", tdiff.total_seconds(), "seconds")
            return result.choices[0].message.content
        except Exception as e:
            rich.print("[bold red]Error[/bold red]: ", e)
            sleep_time = 5
            for i in range(sleep_time):
                rich.print(
                    f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds..."
                )
                sleep(1)


def log_chat(messages, chatlog_dir="chatlogs"):
    index = 0
    # verify directory exists
    if not os.path.exists(chatlog_dir):
        os.makedirs(chatlog_dir)
    filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    while os.path.exists(filename):
        index += 1
        filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    with open(filename, "w") as f:
        rich.print("[bold purple]Info[/bold purple]: writing chatlog to", filename)
        f.write(json.dumps(messages, indent=4))


def print_token_count(messages):
    token_count = 0
    for msg in messages:
        token_count += len(msg["content"])
    rich.print("[bold purple]Info[/bold purple]: current tokens used:", token_count)


def print_num_messages(messages):
    rich.print("[bold purple]Info[/bold purple]: current messages:", len(messages))


# def print_response(response):
# rich.print("[bold blue]ChatGPT[/bold blue]:", response, "\n")


# def main_loop(model, messages):
#    response = send_message(model, messages)
#    messages.append(create_chat_message("assistant", response))
#    print_response(response)
#    while True:
#        lines = []
#        rich.print("[bold]You[/bold]: ", end="")
#        input_msg = ""
#        try:
#            input_msg = input()
#        except EOFError:
#            break
#        if input_msg in ("exit", "quit"):
#            break
#        one_newline_entered = False
#        double_newline_entered = False
#        while double_newline_entered == False:
#            if input_msg == "":
#                one_newline_entered = True
#            lines.append(input_msg)
#            input_msg = input()
#            if input_msg == "" and one_newline_entered == True:
#                double_newline_entered = True
#        input_msg = "\n".join(lines).strip()
#        if input_msg in ("exit", "quit"):
#            break
#        if input_msg in ("clear", "cls", "c"):
#            messages.clear()
#            messages.append(create_chat_message("system", prompt))
#            continue
#        if input_msg in ("tokens", "t"):
#            print_token_count(messages)
#            continue
#        if input_msg in ("write", "w"):
#            filename = input("filename: ")
#            with open(filename, "w") as f:
#                f.write(messages[-1]["content"])
#            continue
#        messages.append(create_chat_message("user", input_msg))
#        response = send_message(model, messages)
#        messages.append(create_chat_message("assistant", response))
#        print_response(response)
#        # print_token_count(messages)
#        # print_num_messages(messages)
#        # print_avg_response_time()
#    log_chat(messages)
#
#
def check_usage():
    if len(sys.argv) != 3:
        print("Usage: python3 pa.py <model> <prompt_filepath>")
        sys.exit(1)


def print_avg_response_time():
    secs = calculate_average_response_time()
    outstr = (
        f"[bold purple]Info[/bold purple]: average response time is {secs:.2f} seconds"
    )
    rich.print(outstr)


def signal_handler(sig, frame):
    # print()
    # log_chat(messages)
    # print_avg_response_time()
    sys.exit(0)


unique_words = {}
unique_groups = {}


def remove_punctuation(word):
    return word.translate(str.maketrans("", "", string.punctuation))


def callback(ch, method, properties, body):
    global messages
    global connection
    body = body.decode("utf-8")
    # print(f"Received {body}")
    # print(f"Them: {body}")
    messages.append(create_chat_message("user", body))
    response = send_message(model, messages)
    messages.append(create_chat_message("assistant", response))
    # print(response)
    if response:
        # at the moment, this part saves a whole sentence
        # we want to split the response into words in a uniform way
        # and get and save a .mp3 for every word
        # this way we can conserve on elevenlabs tokens long-term
        response = response.lower().strip()
        split_response = response.split(" ")
        # console.log(f"{response}")
        unique_words_this_response = 0
        unique_groups_this_response = 0

        for i in range(len(split_response)):
            word = split_response[i]
            word = remove_punctuation(word)
            split_response[i] = word
        # how can i group the words in groups of 4?
        grouped_words = []
        group_len = 4
        for i in range(0, len(split_response), group_len):
            group = split_response[i : i + group_len]
            group = " ".join(group)
            grouped_words.append(group)

        for group in grouped_words:
            # for word in split_response:
            # check if word is in unique_words
            # word_model = f"{model}:{word}"
            group_model = f"{model}:{group}"
            # encoded_word = word_model.encode("utf-8")
            encoded_group = group_model.encode("utf-8")
            hash_object = hashlib.sha256(encoded_group)
            hex_dig = hash_object.hexdigest()
            group_filename = f"audio/{hex_dig}.mp3"

            if os.path.exists(group_filename) and group not in unique_groups:
                unique_groups[group] = True
                # unique_groups_this_response += 1
            elif group not in unique_groups:
                # save group to unique_groups
                unique_groups[group] = True
                # get audio for group
                audio = elevenlabs_client.text_to_speech.convert(
                    text=group,
                    voice_id=f"{voice_model_id}",
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                # save audio
                if not os.path.exists(group_filename):
                    save(audio, group_filename)
                unique_groups_this_response += 1

            # play audio
            # os.system(f"mpg123 {word_filename} 1>/dev/null 2>/dev/null")
        # after saving and processing all the words, we want to join their sound files into a single .mp3
        # we need to construct an ffmpeg command to join the files
        # example: ffmpeg -i "concat:audio1.mp3|audio2.mp3" -acodec copy output.mp3
        # we can use the subprocess module to run the command
        console.print(f"--------------------")
        console.log(
            f"[bold green]Unique groups this response:[/bold green] {unique_groups_this_response}"
        )
        console.log(
            f"[bold purple]Total groups this response:[/bold purple] {len(grouped_words)}"
        )
        console.log(f"[bold blue]Unique groups total:[/bold blue] {len(unique_groups)}")
        # console.log(f"{response}")
        console.print(f"{response}")

        cmd_input = f"concat:"
        # for word in split_response:
        for group in grouped_words:
            # word_model = f"{model}:{word}"
            group_model = f"{model}:{group}"
            encoded_group = group_model.encode("utf-8")
            hash_object = hashlib.sha256(encoded_group)
            hex_dig = hash_object.hexdigest()
            group_filename = f"audio/{hex_dig}.mp3"
            # encoded_word = word_model.encode("utf-8")
            # hash_object = hashlib.sha256(encoded_word)
            # hex_dig = hash_object.hexdigest()
            # word_filename = f"audio/{hex_dig}.mp3"
            cmd_input += f"{group_filename}|"
        cmd_input = cmd_input[:-1]
        sentence = f"{model}:{response}"
        sentence_hash = hashlib.sha256(sentence.encode("utf-8")).hexdigest()
        sentence_filename = f"audio/{sentence_hash}.mp3"
        cmd_output = f'ffmpeg -i "{cmd_input}" -acodec copy {sentence_filename} 1>/dev/null 2>/dev/null'
        os.system(cmd_output)
        # play audio
        os.system(f"mpg123 {sentence_filename} 1>/dev/null 2>/dev/null")

        # console.log(f"{response}")
        ch.basic_publish(exchange="", routing_key=ch2, body=response)
        assert connection
        connection.sleep(SLEEP_TIME)

        # encoded_response = response.encode("utf-8")
        # hash_object = hashlib.sha256(encoded_response)
        # hex_dig = hash_object.hexdigest()
        ## print(hex_dig)
        # audio_filename = f"audio/{hex_dig}.mp3"
        # text_filename = f"text_responses/{hex_dig}.txt"
        ## check if file exists
        # if os.path.exists(text_filename):
        #    with open(text_filename, "r") as f:
        #        response = f.read()
        # else:
        #    with open(text_filename, "w") as f:
        #        f.write(response)
        #        audio = elevenlabs_client.text_to_speech.convert(
        #            text=response,
        #            voice_id=f"{voice_model_id}",
        #            model_id="eleven_multilingual_v2",
        #            output_format="mp3_44100_128",
        #        )
        #        save(audio, audio_filename)
        # console.log(f"{response}")
        # os.system(f"mpg123 {audio_filename} 1>/dev/null 2>/dev/null")
        # ch.basic_publish(exchange="", routing_key=ch2, body=response)
        # assert connection
        # connection.sleep(SLEEP_TIME)


def main():
    global messages
    global model
    global connection
    # model = initialize_openai()
    # set up pika connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue=ch1)
    channel.queue_declare(queue=ch2)

    # clear messages
    channel.queue_purge(queue=ch1)
    channel.queue_purge(queue=ch2)

    signal.signal(signal.SIGINT, signal_handler)  # ctrl-c
    # check_usage()
    prompt = initialize_prompt(prompt_filename)
    messages = [create_chat_message("system", prompt)]

    response = send_message(model, messages)
    if response and send_initial_response:

        response_salted = f"{model}:{response}"
        encoded_response = response_salted.encode("utf-8")
        hash_object = hashlib.sha256(encoded_response)
        hex_dig = hash_object.hexdigest()
        # print(hex_dig)
        audio_filename = f"audio/{hex_dig}.mp3"
        text_filename = f"text_responses/{hex_dig}.txt"
        # check if file exists
        if os.path.exists(text_filename):
            with open(text_filename, "r") as f:
                response = f.read()
                # os.system(f"mpg123 {audio_filename} 1>/dev/null 2>/dev/null")
        else:
            with open(text_filename, "w") as f:
                f.write(response)

                audio = elevenlabs_client.text_to_speech.convert(
                    text=response,
                    voice_id=f"{voice_model_id}",
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                save(audio, audio_filename)
                # os.system(f"mpg123 {audio_filename} 1>/dev/null 2>/dev/null")

        print(f"{response}")
        os.system(f"mpg123 {audio_filename} 1>/dev/null 2>/dev/null")
        messages.append(create_chat_message("assistant", response))
        channel.basic_publish(exchange="", routing_key=ch2, body=response)

    # wait for channel message back
    channel.start_consuming()

    with console.status(f"[bold green]{model} is running...[/bold green]"):
        try:
            while True:
                channel.basic_consume(
                    queue=ch1, on_message_callback=callback, auto_ack=True
                )
                connection.process_data_events()
                connection.sleep(SLEEP_TIME)
        except Exception as e:
            print(e)
    channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()
