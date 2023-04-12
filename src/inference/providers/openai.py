import os
import openai

from quintus import Quintus
from utils.loading import loading_animation
from templates.prompts import Prompts

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model_engine = "gpt-3.5-turbo"

quintus = Quintus()
prompts = Prompts(quintus)


def send_system_message(messages):
    response = openai.ChatCompletion.create(model=model_engine, messages=messages)
    return response


def chat():
    messages = [
        {"role": "system", "content": prompts.system_prompt_test("The company")},
    ]
    send_system_message(messages)
    while True:
        user_input = input("👤: ")
        message = prompts.context_prompt(user_input)

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
            print(
                "Type 'quit' to exit the chat, 'clear' to clear the chat history, 'history' to view the chat history, and 'help' to view this message."
            )
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


if __name__ == "__main__":
    chat()
