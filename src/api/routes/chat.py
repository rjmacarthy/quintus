from fastapi.encoders import jsonable_encoder
from api.services.chat import ChatService


class ChatRoutes:
    def __init__(self, app):
        self.app = app

    def register(app):
        chat_service = ChatService().get_instance()

        @app.post("/chat/create_chat")
        def create_chat():
            return chat_service.create_chat()

        @app.post("/chat/{chat_id}/add_message")
        def add_message(chat_id: str):
            return chat_service.add_message(
                chat_id=id, message=app.request.json(["message"])
            )

        @app.get("/chat/{id}")
        def get_chat(id: str):
            chat = chat_service.get_chat(id)
            return jsonable_encoder(chat)

        @app.get("/ping")
        def ping():
            return "pong"
