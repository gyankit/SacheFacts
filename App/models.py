from App import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


class Admin(db.Model, UserMixin):
    __tableanme__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'username : { self.username }, email : { self.email }'


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('PostTag', backref='tag', lazy=True)

    def __repr__(self):
        return f'id : { self.id }, name : { self.name }'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('PostCategory', backref='category', lazy=True)

    def __repr__(self):
        return f'id : { self.id }, name : { self.name }'


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=True, nullable=False)
    slag = db.Column(db.String(500), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    youtube = db.Column(db.String(500))
    facebook = db.Column(db.String(500))
    instagram = db.Column(db.String(500))
    link1 = db.Column(db.String(500))
    link2 = db.Column(db.String(500))
    thumbnail = db.Column(db.String(500), nullable=False)
    video = db.Column(db.String(500))
    status = db.Column(db.Boolean, nullable=False, default=True)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    tags = db.relationship('PostTag', backref='post', lazy=True)
    categories = db.relationship('PostCategory', backref='post', lazy=True)

    def __repr__(self):
        return f'id : {self.id }, title : { self.title }'


class PostTag(db.Model):
    __tablename__ = 'post_tag'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)

    def __repr__(self):
        return f'post : { self.post_id }, tag : { self.tag_id }'


class PostCategory(db.Model):
    __tablename__ = 'post_category'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'post : { self.post_id }, category : { self.category_id }'


class PostImage(db.Model):
    __tablename__ = 'post_images'
    id = db.Column(db.Integer, primary_key=True)
    slag = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'slag : { self.slag }, image : { self.image }'


class AccountSetting(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(500), nullable=False, unique=True)
    site_logo = db.Column(db.String(500), nullable=False, unique=True)
    site_poster = db.Column(db.String(500), nullable=False, unique=True)
    admin_firstname = db.Column(db.String(50), nullable=False, unique=True)
    admin_lastname = db.Column(db.String(50), nullable=False, unique=True)
    admin_displayname = db.Column(db.String(100), nullable=False, unique=True)
    admin_contact = db.Column(db.String(15), nullable=False, unique=True)
    admin_email = db.Column(db.String(50), nullable=False, unique=True)
    admin_address = db.Column(db.String(500))
    admin_photo = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return f'id : { self.id }'