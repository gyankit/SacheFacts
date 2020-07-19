from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField, SelectMultipleField, MultipleFileField, HiddenField
from wtforms.validators import DataRequired, Optional, URL, ValidationError, Email, EqualTo, Length
from App.models import Tag, Category, Admin


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder':'Username'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        if Tag.query.filter_by(name=name.data).first():
            raise ValidationError('Duplicate Entry!')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        if Category.query.filter_by(name=name.data).first():
            raise ValidationError('Duplicate Entry!')


class DeleteForm(FlaskForm):
    deleteid = HiddenField()
    delete = SubmitField('Delete')


class NonValidatingSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass


class PostCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    youtube = StringField('Youtube', validators=[Optional(), URL()])
    facebook = StringField('Facebook', validators=[Optional(), URL()])
    instagram = StringField('Instagram', validators=[Optional(), URL()])
    link1 = StringField('Extra link1', validators=[Optional(), URL()])
    link2 = StringField('Extra link2', validators=[Optional(), URL()])
    selectcategory = NonValidatingSelectMultipleField('Categories', validators=[Optional()], choices=[], render_kw={'data-placeholder':'Select Categories'})
    category = StringField('Add Categories', validators=[Optional()])
    selecttag = NonValidatingSelectMultipleField('Tags', validators=[Optional()], choices=[], render_kw={'data-placeholder':'Select Tags'})
    tag = StringField('Add Tags', validators=[Optional()])
    thumbnail = FileField('Thumbnail', validators=[FileRequired(), FileAllowed(['PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg'], 'valid image required ( PNG / JPG / JPEG )')], render_kw={'accept':'image/*'})
    featured = BooleanField('Add to Featured Group')
    submit = SubmitField('Submit')
    '''video = MultipleFileField('Videos ( Multiple )', validators=[Optional(), FileAllowed(['MP4', 'mp4', '3GP', '3gp', 'AVI', 'avi', 'WEBM', 'webm', 'WMV', 'wmv'], 'valid videos required ( MP4 / AVI / WEBM / WMV / 3GP )')])'''


class AccountForm(FlaskForm):
    site_title = StringField('Site Title', validators=[DataRequired()])
    site_logo = FileField('Sile Logo', validators=[Optional(), FileAllowed(['PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg'], 'valid image required ( PNG / JPG / JPEG )')], render_kw={'accept':'image/*'})
    site_poster = FileField('Site Poster', validators=[Optional(), FileAllowed(['PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg'], 'valid image required ( PNG / JPG / JPEG )')], render_kw={'accept':'image/*'})
    site_youtube = StringField('Site Youtube Link', validators=[DataRequired(), URL()])
    site_facebook = StringField('Site Facebook Link', validators=[DataRequired(), URL()])
    site_instagram = StringField('Site Instagram Link', validators=[DataRequired(), URL()])
    admin_firstname = StringField('Admin Firstname', validators=[DataRequired()])
    admin_lastname = StringField('Admin Lastname', validators=[DataRequired()])
    admin_displayname = StringField('Admin Displayname', validators=[DataRequired()])
    admin_contact = StringField('Admin Contact No.', validators=[DataRequired()])
    admin_email = StringField('Admin Email Id', validators=[DataRequired()])
    admin_address = StringField('Admin Address', validators=[Optional()])
    admin_photo = FileField('Admin Photo', validators=[Optional(), FileAllowed(['PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg'], 'valid image required ( PNG / JPG / JPEG )')], render_kw={'accept':'image/*'})
    update = SubmitField('Update')


class ProfileLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=8, max=20)], render_kw={'placeholder':'Password'})
    confirmpassword = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password', 'Both Passwords not Matched.')], render_kw={'placeholder':'Confirm Password'})
    key = HiddenField('key', validators=[DataRequired()])
    submit = SubmitField('Update')


class PasswordForgetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    submit = SubmitField('Request New Password')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data, role='admin').first()
        if admin is None:
            raise ValidationError('There is no acocunt with that email. you must register first.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)], render_kw={'placeholder':'Password'})
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Both Passwords not Matched.'), Length(min=8, max=20)], render_kw={'placeholder':'Confirm Password'})
    submit = SubmitField('Confirm Change Password')
