from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Enter the username, please"),
                                Length(3, 24, message="Too long or short username")])
    email = StringField("Email", validators=[DataRequired(message="Enter the email, please"),
                                Email(message="Email is incorrect")])
    password = PasswordField("Password", validators=[DataRequired(message="Enter the password, please"),
                                Length(3, 24, message="Too long or short password"),
                                EqualTo("confirm", message="Your password is not equal to the confirmation password")])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(message="Enter the password, please"),
                                Length(3, 24, message="Too long or short password")])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(message="Enter the email, please"),
                                                     Email(message="Email is incorrect")])
    password = PasswordField("Password", validators=[DataRequired(message="Enter the password, please"),
                                                     Length(3, 24, message="Too long or short password")])


class SettingsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Enter the username, please"),
                                                   Length(3, 24, message="Too long or short username")])
    profile_picture = FileField("Profile Picture", validators=[FileAllowed(["png", "jpg", "jpeg"], "Only images!")])
