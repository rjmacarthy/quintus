import os
import openai
import time

from templates.prompts import Prompts
from inference.tasks.chat import Chat

openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "gpt-3.5-turbo"


class OpenAIChat(Chat):
    def __init__(self, prompts: Prompts):
        super().__init__(prompts)

    def send_system_message(self, messages):
        response = openai.ChatCompletion.create(model=model_engine, messages=messages)
        return response

    def chat(self):
        messages = [
            {"role": "system", "content": self.prompts.system_prompt("The company")}
        ]
        self.send_system_message(messages)
        while True:
            reply = None
            user_input = input("👤: ")
            message = user_input.lower().strip()

            if message == "quit":
                break

            if message == "clear":
                messages = []
                self.send_system_message(messages)
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
                self.add_message(message, "user")
                prompt = self.prompts.context_prompt(user_input, "The company")
                messages.append({"role": "user", "content": prompt})

                print("🤖: Thinking...")

                completion = openai.ChatCompletion.create(
                    model=model_engine,
                    messages=messages,
                )

                reply = completion["choices"][0]["message"]["content"]

                time.sleep(2)

                print(f"\033[F\033[K🤖: {reply}")

                self.add_message(reply, "assistant")

                messages.append({"role": "assistant", "content": reply})
