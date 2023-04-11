from flask import Blueprint, render_template, flash, redirect, url_for, request
from apps.messenger.models import Chat, Message
from database.database import db
from flask_login import current_user
from utils import get_image_name_by_id, UPLOAD_FOLDER

messenger = Blueprint("messenger", __name__, template_folder="templates/messenger")
def get_main_chat():
    return db.session.query(Chat).get(1)

@messenger.route("/")
def index():
    main_chat = get_main_chat()
    if not main_chat:
        main_chat = Chat()
        db.session.add(main_chat)
        db.session.commit()
    return render_template("index.html", chat=main_chat,
                           get_image=get_image_name_by_id,
                           path=UPLOAD_FOLDER
                           )

@messenger.route("/send_message", methods=["POST"])
def send_message():
    msg = request.form['msg']
    if msg == '':
        return redirect(url_for("messenger.index"))
    if len(msg) > 200:
        flash("too many characters, max-200")
        return redirect(url_for("messenger.index"))
    chat = get_main_chat()
    message = Message(author=current_user, chat=chat, text=msg)
    chat.add_message(message)
    db.session.add(message)
    db.session.commit()
    return redirect(url_for("messenger.index"))
