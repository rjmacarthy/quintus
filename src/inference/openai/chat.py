import openai
import time

from inference.base.chat import Chat
from inference.openai.model import OpenAIModel
from prompts.prompts import Agents


class OpenAIChat(Chat):
    def __init__(self):
        super().__init__()
        self.agents = Agents()
        self.model = OpenAIModel()

    def send_system_message(self, messages):
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response

    def chat(self, entity="user"):
        while True:
            message = input("👤: ")

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
                context = self.agents.get_context(message)
                reply = self.agents.assistant(
                    entity=entity, context=context, question=message
                )
                message = reply["reply"]
                print(f"🤖: {message}")
