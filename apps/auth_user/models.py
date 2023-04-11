from datetime import datetime
from database.database import db
from utils import bcrypt
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id =                db.Column(      db.Integer(),       primary_key=True)
    name =              db.Column(      db.String(24),      nullable=False)
    email =             db.Column(      db.String(150),     nullable=False)
    password =          db.Column(      db.String(150),     nullable=False)
    registered_on =      db.Column(      db.DateTime(),      default=datetime.now)

    def __repr__(self):
        return f"id: {self.id}\nname: {self.name}\nemail: {self.email}"

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("UTF-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

