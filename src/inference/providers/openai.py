import os
import openai

from templates.simple import simple_prompt
from templates.system import system_prompt
from store import Store
from utils.loading import loading_animation

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model_engine = "gpt-3.5-turbo"


def send_system_message(messages):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages
    )
    return response


def start():
    messages = [
        {"role": "system", "content": system_prompt("The company")},
    ]
    send_system_message(messages)
    store = Store()
    while True:
        user_input = input("👤: ")
        message = simple_prompt(user_input, store)

        if message == "quit":
            break

        if message == "clear":
            messages = []
            send_system_message(messages)
            continue

        if message == "history":
            print(messages)
            continue

        if message == "help":
            print("Type 'quit' to exit the chat, 'clear' to clear the chat history, 'history' to view the chat history, and 'help' to view this message.")
            continue

        if message:
            messages.append({"role": "user", "content": message})
            loading_animation()
            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages=messages,
            )
            reply = completion["choices"][0]["message"]["content"]
            print(f"🤖: {reply}")
            messages.append({"role": "assistant", "content": reply})
