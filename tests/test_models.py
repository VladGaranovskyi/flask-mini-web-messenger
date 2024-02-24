import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

import unittest
from flask import Flask
from database import database
from database.database import db
from apps.auth_user.models import User
from apps.messenger.models import Chat, Message
from datetime import datetime
from utils import init_bcrypt, init_login_manager

class TestModels(unittest.TestCase):
    def setUp(self):
        # Setup database for testing
        app = Flask(__name__)
        app.config.from_object('config.DevelopmentConfig')
        init_login_manager(app)
        init_bcrypt(app)
        database.init_app_db(app)

    def tearDown(self):
        # Clean up database after testing
        db.session.remove()
        db.drop_all()

    def test_add_message_to_chat(self):
        # Create a user
        user = User(name="Test User", email="test@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        # Create a chat
        chat = Chat()
        db.session.add(chat)
        db.session.commit()

        # Add a message to the chat
        message = Message(chat_id=chat.id, author_id=user.id, text="Test message")
        db.session.add(message)
        db.session.commit()

        # Check if the message was added to the chat
        self.assertEqual(len(chat.messages), 1)
        self.assertEqual(chat.messages[0].text, "Test message")

    def test_change_messages_limit(self):
        # Create a chat
        chat = Chat()
        db.session.add(chat)
        db.session.commit()

        # Change the messages limit
        chat.change_limit(100)

        # Check if the messages limit was changed
        self.assertEqual(chat._Chat__messages_limit, 100)

    def test_user_creation(self):
        # Create a user
        user = User(name="Test User", email="test@example.com", password="password")

        # Check if the user was created correctly
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password"))
        self.assertIsInstance(user.registered_on, datetime)

if __name__ == '__main__':
    unittest.main()
