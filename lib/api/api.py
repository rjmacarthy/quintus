import time
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

import uvicorn

from database.repository import Repository
from database.chat_repository import ChatRepository
from database.schema.document import Document
from database.schema.message import Message
from prompts import Prompts
from lib.inference.openai.model import get_completion


class Api:
    def __init__(self) -> None:
        self.document_repository = Repository(Document)
        self.chat_repository = ChatRepository()
        self.message_repository = Repository(Message)
        self.prompts = Prompts()
        self.app = FastAPI()

    def serve(self):
        app = FastAPI()

        def build_conversation_history(chat_id: str):
            messages = []
            for message in self.chat_repository.get_messages(chat_id):
                messages.append(
                    {
                        "role": message.entity,
                        "content": message.message,
                    }
                )
            return messages

        @app.get("/completion")
        def completion(query: str, id: str):
            chat = self.chat_repository.get_by_id(id)
            if chat is not None:
                messages = build_conversation_history(id)
            else:
                messages = []

            message = self.prompts.context_prompt(query, "user")
            messages.append({"role": "system", "content": message})
            self.message_repository.create(
                message=message, time=time.time(), chat_id=self.chat_id, entity="user"
            )
            response = get_completion(messages)
            self.message_repository.create(
                message=response,
                time=time.time(),
                chat_id=self.chat_id,
                entity="assistant",
            )
            return response

        @app.get("/chat/{id}")
        def get_chat(id: str):
            messages = self.chat_repository.get_messages(id)
            return jsonable_encoder(messages)

        @app.get("/ping")
        def ping():
            return "pong"

        uvicorn.run(app, host="0.0.0.0", port=8000)
