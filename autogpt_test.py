import requests
import sys
import bs4
import openai
import os
from datetime import datetime
from rich import print


messages = []
response_times = []
responses = []


def initialize_openai():
    openai.organization = 'evildojo'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    #if sys.argv[2] == 'gpt-3.5-turbo-0301':
    #if 'gpt-3' in sys.argv[2] or 'gpt3' in sys.argv[2]:
    return 'gpt-3.5-turbo'
    #if 'gpt-4' in sys.argv[2] or 'gpt4' in sys.argv[2]:
    #    return 'gpt-4'
    # error out 
    #print("[bold red]Error[/bold red]: invalid model")
    #print("Error: invalid model")
    #sys.exit(1)


def create_chat_message(role, content):
    return {'role': role, 'content': content}


def send_message(model, messages):
    t0 = datetime.now()
    while True:
        try:
            result = openai.ChatCompletion.create(model=model, messages=messages)
            t1 = datetime.now()
            tdiff = t1 - t0
            response_times.append(tdiff.total_seconds())
            #print("[bold purple]Info[/bold purple]: message sent in", tdiff.total_seconds(), "seconds")
            return result["choices"][0]["message"]["content"]
        except InvalidRequestError as e:
            print("[bold red]Error[/bold red]: ", e)
            sleep_time = 30
            for i in range(sleep_time):
                rich.print(f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds...")
                sleep(1)
        except Exception as e:
            print("[bold red]Error[/bold red]: ", e)
            sleep_time = 10
            for i in range(sleep_time):
                rich.print(f"[bold purple]Info[/bold purple]: sleeping for {sleep_time-i} seconds...")
                sleep(1)


def log_chat(messages, chatlog_dir="autogpt_test_chatlogs"):
    index = 0
    filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    while os.path.exists(filename):
        index += 1
        filename = os.path.join(chatlog_dir, f"chatlog{index}.json")
    with open(filename, "w") as f:
        f.write(json.dumps(messages, indent=4))



def main():
    if len(sys.argv) < 2:
        print("Usage: python autogpt_test.py <url>")
        sys.exit(1)
    url = sys.argv[1]

    print("Scraping URL...")
    r = requests.get(url)
    print("Parsing text...")
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    text = ' '.join(map(lambda p: p.text, soup.find_all()))
    text = text.encode('ascii', errors='replace').decode('utf-8')
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = text.replace('"', '')
    text = text.replace("'", '')
    print("Splitting text into chunks...")

    text_chunk_size = 2048
    text_chunks = [text[i:i+text_chunk_size] for i in range(0, len(text), text_chunk_size)]

    print("Initializing OpenAI...")
    model = initialize_openai()
    prompt = "Please summarize the following text blobs which were scraped from a website, I will present them in the following messages one at a time."
    messages = [create_chat_message('system', prompt)]

    for i in range(len(text_chunks)):
        print("Sending chunk", i+1, "of", len(text_chunks))
        messages.append(create_chat_message('user', text_chunks[i]))
        response_txt = send_message(model, messages)
        #print(response_txt)
        #messages.append(create_chat_message('assistant', response_txt))
        responses.append(response_txt)
        # delete this text chunk from the messages
        messages.pop()
        #print("-"*10)

    # Now that we have a list of summaries, we need to summarize the summaries
    # join together all of the responses into a single text string
    print("Sending last chunk...")
    all_response_txt = ' '.join(responses)
    messages.append(create_chat_message('user', all_response_txt))
    response_txt = send_message(model, messages)

    print(response_txt)

    #for response in responses:
    #    print(response, '\n')




if __name__ == '__main__':
    main()

