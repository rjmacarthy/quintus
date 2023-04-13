import os
import openai
import time
import threading
import sys
import itertools


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model_engine = "gpt-3.5-turbo"


def send_system_message(messages):
    response = openai.ChatCompletion.create(model=model_engine, messages=messages)
    return response


def chat(prompts):
    messages = [{"role": "system", "content": prompts.system_prompt("The company")}]
    send_system_message(messages)
    while True:
        reply = None
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
            done = False

            def animate():
                for c in itertools.cycle(["|", "/", "-", "\\"]):
                    if done:
                        break
                    sys.stdout.write("\rloading " + c)
                    sys.stdout.flush()
                    sys.stdout.write("\r")
                    time.sleep(0.1)

            t = threading.Thread(target=animate)
            t.start()

            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages=messages,
            )
            reply = completion["choices"][0]["message"]["content"]
            print(f"🤖: {reply}")
            messages.append({"role": "assistant", "content": reply})

            done = True


if __name__ == "__main__":
    chat()
