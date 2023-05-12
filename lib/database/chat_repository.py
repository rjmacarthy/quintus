from database.repository import Repository
from database.schema.chat import Chat
from database.schema.message import Message


class ChatRepository(Repository):
    def __init__(self):
        super().__init__(Chat)

    def get_messages(self, id: str):
        with self.session() as session:
            return session.query(Message).filter(Message.chat_id == id).all()
