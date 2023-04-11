from database.database import db


class Chat(db.Model):
    __tablename__ = "chats"
    __messages_limit = 50

    id =                db.Column(      db.Integer(),       primary_key=True)
    messages =          db.relationship("Message",          back_populates="chat")

    def add_message(self, msg):
        if len(self.messages) > self.__messages_limit:
            self.messages.pop(0)
        self.messages.append(msg)

    def __repr__(self):
        return "\n".join([f"{m.author.name}: {m.text}" for m in self.messages])

    def change_limit(self, new_limit):
        self.__messages_limit = new_limit


class Message(db.Model):
    __tablename__ = "messages"

    id =        db.Column(    db.Integer(),       primary_key=True)
    chat_id =   db.Column(    db.Integer(),       db.ForeignKey("chats.id"))
    author_id = db.Column(    db.Integer(),       db.ForeignKey("users.id"))
    text =      db.Column(    db.String(200),     nullable=False)

    chat = db.relationship("Chat", back_populates="messages", uselist=False)
    author = db.relationship("User", uselist=False)
