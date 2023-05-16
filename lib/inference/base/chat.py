import time

from database.schema.message import Message
from database.schema.chat import Chat as ChatSchema
from database.repository import Repository
from prompts.prompts import Prompts
from lib.inference.local.summarizer import Summarization
from lib.inference.local.entity_extractor import EntityExtractor


class Chat:
    def __init__(self, prompts: Prompts):
        self.prompts = prompts
        self.chat_repository = Repository(ChatSchema)
        self.message_repository = Repository(Message)
        self.summarization = Summarization("facebook/bart-large-cnn")
        self.entity_extractor = EntityExtractor("dslim/bert-base-NER")
        self.chat_id = self.create()

    def create(self) -> int:
        chat = self.chat_repository.create()
        self.chat_id = chat.id
        print(f"Welcome! Your chat id is: {chat.id} how can I help you?")
        return chat.id

    def message(self, message, entity):
        self.message_repository.create(
            message=message, time=time.time(), chat_id=self.chat_id, entity=entity
        )

    def transcript(self, messages) -> str:
        return "\n".join(
            [f"{message['role']}: {message['content']}" for message in messages[:3]]
        )

    def summarize(self, messages) -> str:
        return self.summarization.run(self.get_transcript(messages))

    def entities(self, messages) -> str:
        return self.entity_extractor.run(self.get_transcript(messages))
