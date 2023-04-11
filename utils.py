from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from database.database import db
from os import listdir, remove
from os.path import isfile

UPLOAD_FOLDER = 'static/profile_images'

login_manager = LoginManager()
login_manager.login_view = "login"

bcrypt = Bcrypt()

def init_login_manager(app):
    login_manager.init_app(app)

def init_bcrypt(app):
    bcrypt.init_app(app)

def get_image_name_by_id(id, upload_folder=UPLOAD_FOLDER):
    names = [f.split(".") for f in listdir(upload_folder) if "_" not in f]
    for name in names:
        if int(name[0]) == id:
            return f"{name[0]}.{name[-1]}"
    return ""

def save_img(img, img_id, upload_folder=UPLOAD_FOLDER):
    if isfile(f"{upload_folder}/{get_image_name_by_id(img_id)}"):
        remove(f"{upload_folder}/{get_image_name_by_id(img_id)}")
    fileName = img.filename.split(".")
    fileName[0] = img_id
    fileName = f"{fileName[0]}.{fileName[-1]}"
    img.save(f"{upload_folder}/{fileName}")