from database.repository import Repository
from database.schema.chat import Chat
from database.schema.message import Message


class ChatRepository(Repository):
    def __init__(self):
        super().__init__(Chat)
        self._instance = None

    def get_instance(self):
        if self._instance is None:
            self._instance = ChatRepository()
        return self._instance

    def get_chat(self, id: str):
        with self.session() as session:
            return (
                session.query(Message)
                .filter(Message.chat_id == id)
                .order_by(Message.time)
                .all()
            )
