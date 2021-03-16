"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class AddUserForm(FlaskForm):
    """Form for adding pets."""

    username = StringField("Username", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginUser(FlaskForm):
    """Form for adding pets."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
