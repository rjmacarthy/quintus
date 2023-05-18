import openai
import time

from inference.base.chat import Chat
from inference.openai.model import OpenAIModel
from prompts.prompts import Prompts


class OpenAIChat(Chat):
    def __init__(self):
        super().__init__()
        self.prompts = Prompts()
        self.model = OpenAIModel()

    def send_system_message(self, messages):
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response

    def chat(self, entity="user"):
        messages = [{"role": "system", "content": self.prompts.system_prompt(entity)}]
        self.send_system_message(messages)
        while True:
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
                self.message(message, "user")
                prompt = self.prompts.context_prompt(user_input, "The company")
                messages.append({"role": "user", "content": prompt})

                print("🤖: Thinking...")

                response = self.model.completion(messages)

                time.sleep(2)

                print(f"\033[F\033[K🤖: {response}")

                self.message(message, "assistant")

                messages.append({"role": "assistant", "content": response})
