from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    fullname = StringField('Name', validators=[DataRequired()])
    email = StringField('Eamil Id', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    send = SubmitField('Send')