from flask import Flask
from database import database
from apps.auth_user.views import auth
from apps.messenger.views import messenger
from utils import init_login_manager, init_bcrypt

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

init_login_manager(app)
init_bcrypt(app)
database.init_app_db(app)

app.register_blueprint(auth)
app.register_blueprint(messenger)

if __name__ == "__main__":
    app.run()
