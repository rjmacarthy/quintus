import time
from fastapi.encoders import jsonable_encoder

from database.chat_repository import ChatRepository
from database.repository import Repository
from database.schema.message import Message
from inference.openai.model import OpenAIModel
from prompts.prompts import Prompts


class ChatService:
    def __init__(self) -> None:
        self.chat_repository = ChatRepository().get_instance()
        self.message_repository = Repository(Message)
        self.prompts = Prompts()
        self.model = OpenAIModel()
        self._instance = None

    def get_instance(self):
        if self._instance is None:
            self._instance = ChatService()
        return self._instance

    def get_chat(self, chat_id: str):
        chat = self.chat_repository.get_chat(chat_id)
        return chat

    def create_chat(self):
        chat = self.chat_repository.create()
        return {"chat_id": chat.id}

    def add_message(self, chat_id, message: str):
        if chat_id is None:
            return {"error": "chat id is required"}
        chat = self.chat_repository.get_chat(chat_id)
        messages = self.get_messages(id)
        message = self.prompts.context_prompt(message, "user")
        messages.append({"role": "system", "content": message})
        self.message_repository.create(
            message=message, time=time.time(), chat_id=chat.id, entity="user"
        )
        model_response = self.model.completion(messages)
        self.message_repository.create(
            message=model_response,
            time=time.time(),
            chat_id=chat.id,
            entity="assistant",
        )
        return {
            "response": model_response,
            "chat_id": chat.id,
        }

    def get_messages(self, chat_id: str):
        messages = []
        for message in self.chat_repository.get_messages(chat_id):
            messages.append(
                {
                    "role": message.entity,
                    "content": message.message,
                }
            )
        return messages
