import time

from database.schema.message import Message
from database.schema.chat import Chat as ChatSchema
from database.repository import Repository
from templates.prompts import Prompts
from inference.tasks.summarization import Summarization
from inference.tasks.ner import NamedEntityRecognition


class Chat:
    def __init__(self, prompts: Prompts):
        self.prompts = prompts
        self.chat_repository = Repository(ChatSchema)
        self.message_repository = Repository(Message)
        self.summarization = Summarization("facebook/bart-large-cnn")
        self.ner = NamedEntityRecognition("dslim/bert-base-NER")
        self.chat_id = self.create()

    def get_transcript(self, messages) -> str:
        return "\n".join(
            [f"{message['role']}: {message['content']}" for message in messages[:3]]
        )

    def summarize(self, messages) -> str:
        return self.summarization.run(self.get_transcript(messages))

    def get_entities(self, messages) -> str:
        return self.ner.run(self.get_transcript(messages))

    def create(self) -> int:
        chat = self.chat_repository.create()
        self.chat_id = chat.id
        print(f"Welcome! Your chat id is: {chat.id} how can I help you?")
        return chat.id

    def add_message(self, message, entity):
        self.message_repository.create(
            message=message, time=time.time(), chat_id=self.chat_id, entity=entity
        )
