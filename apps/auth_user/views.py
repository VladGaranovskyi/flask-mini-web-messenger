from flask import Blueprint, render_template, flash, redirect, url_for, request
from apps.auth_user.forms import RegisterForm, LoginForm, SettingsForm
from apps.auth_user.models import User
from database.database import db
from flask_login import current_user, login_user, login_required, logout_user
from utils import login_manager, save_img

auth = Blueprint("auth", __name__, template_folder="templates/auth")

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("messenger.index"))
    else:
        if form.email.errors:
            for e in form.email.errors:
                flash(e)
        if form.password.errors:
            for e in form.password.errors:
                flash(e)
    return render_template("login.html", form=form)

@auth.route("/sign_up", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if db.session.query(User).filter(User.email == form.email.data).first():
            flash("The user with this email already exists")
            return redirect(url_for("auth.register"))
        new_user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        new_user = db.session.query(User).filter(User.name == form.username.data).first()
        login_user(new_user)
        return redirect(url_for("auth.settings"))
    else:
        if form.username.errors:
            for e in form.username.errors:
                flash(e)
        if form.email.errors:
            for e in form.email.errors:
                flash(e)
        if form.password.errors:
            for e in form.password.errors:
                flash(e)
        if form.confirm.errors:
            for e in form.confirm.errors:
                flash(e)

    return render_template("register.html", form=form)

@auth.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()
    if request.method == "GET":
        form.username.data = current_user.name
    if form.validate_on_submit():
        current_user.name = form.username.data
        user = db.session.query(User).filter(User.name == current_user.name).first()
        user.name = form.username.data
        if form.profile_picture.data:
            save_img(form.profile_picture.data, user.id)
        db.session.commit()
        return redirect(url_for("messenger.index"))
    else:
        if form.username.errors:
            for e in form.username.errors:
                flash(e)
        if form.profile_picture.errors:
            for e in form.profile_picture.errors:
                flash(e)
    return render_template("settings.html", form=form, username=current_user.name)

@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("messenger.index"))
