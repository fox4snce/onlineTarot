import openai
import time
from http.client import RemoteDisconnected
from tokens import TokenManager

tm = TokenManager()

def send_message_to_openai(messages):
    while True:
        try:
            time.sleep(1)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            print("\n\nSpeaking to gpt... ")
            
            content = response.choices[0].message['content']
            
            tm.update_tokens(response['usage']['total_tokens'])
            tm.print_totals()

            print("Returning response...\n", content, "\n\n")
            return content

        except openai.error.RateLimitError:
            print("Rate limit exceeded. Waiting 2 seconds...")
            time.sleep(2)
        except RemoteDisconnected:
            print("Remote end closed connection without response. Retrying in 5 seconds...")
            time.sleep(5)

def send_message_with_guard(messages, guard):
    while True:
        try:
            #time.sleep(1)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            print("\n\nSpeaking to gpt... ")
            
            content = response.choices[0].message['content']
            
            tm.update_tokens(response['usage']['total_tokens'])
            tm.print_totals()

            print("Returning response...\n", content, "\n\n")
            return content

        except openai.error.RateLimitError:
            print("Rate limit exceeded. Waiting 2 seconds...")
            time.sleep(2)
        except RemoteDisconnected:
            print("Remote end closed connection without response. Retrying in 5 seconds...")
            time.sleep(5)


def compress_text(text):

    print("Compressing text... " + text)
    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "compress the following text such that you (GPT) can reconstruct the intention of the human who wrote text as close as possible to the original intention. This is for yourself. It does not need to be human readable or understandable. Abuse of language mixing, abbreviations, symbols (unicode and emoji), or any other encodings or internal representations is all permissible, as long as it, if pasted in a new inference cycle, will yield near-identical results as the original text.\n ### Text to compress:\n"},
    {"role": "user", "content": text}
    ]

    response = send_message_to_openai(messages)
    compressed_text = response.strip()

    return compressed_text




def template(some_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Text text: {some_input}"}
    ]
    output = send_message_to_openai(messages)
    return output