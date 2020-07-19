from App import db
from App.users import user
from flask import render_template, redirect, url_for, request, abort, jsonify, flash
from App.models import Post, Tag, Category, PostImage, PostCategory, PostTag, AccountSetting, Subscriber
from App.users.forms import ContactForm
import json


#Home Page Route
@user.route('/')
def home():
    title = 'SacheFacts | Home'
    site = AccountSetting.query.get(1)
    if site is None:
        abort(500)
    latest = Post.query.filter_by(status=True).order_by(Post.created_at.desc()).limit(5)
    featured = Post.query.filter_by(featured=True, status=True).all()
    tags = Tag.query.all()
    categories = Category.query.all()
    posttags = PostTag.query.all()
    postcategories = PostCategory.query.all()
    return render_template('user/home.html', title=title, site=site, latest=latest, featured=featured, tags=tags, categories=categories, posttags=posttags, postcategories=postcategories)


#About Page Route
@user.route('/about')
def about():
    title = 'SacheFacts | AboutUs'
    site = AccountSetting.query.get(1)
    if site is None:
        abort(500)
    return render_template('user/about.html', title=title, site=site)


#Contact Page Route
@user.route('/contact', methods=['GET', 'POST'])
def contact():
    title = 'SacheFacts | Contact'
    site = AccountSetting.query.get(1)
    if site is None:
        abort(500)
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        print(request.form)
        flash('Message Successfully Sent!', 'contact')
        return redirect(url_for('users.contact'))
    return render_template('user/contact.html', title=title, site=site, form=form)


#Blogs Page Route
@user.route('/blogs')
def blogs():
    title = 'SacheFacts | Blog'
    site = AccountSetting.query.get(1)
    if site is None:
        abort(500)
    if request.args.get('page'):
        if int(request.args.get('page')) > 0:
            page = int(request.args.get('page'))
        else:
            abort(404)
    else:
        page=1
    per_page=5
    blogs = Post.query.filter_by(status=True).order_by(Post.created_at.desc()).paginate(page, per_page)
    featured = Post.query.filter_by(featured=True, status=True).all()
    tags = Tag.query.all()
    categories = Category.query.all()
    posttags = PostTag.query.all()
    postcategories = PostCategory.query.all()
    return render_template('user/blogs.html', title=title, site=site, blogs=blogs, featured=featured, tags=tags, categories=categories, posttags=posttags, postcategories=postcategories)


#Single Blog Page Route
@user.route('/blog/<slag>')
def singleblog(slag):
    title = f'SacheFacts | { slag }'
    site = AccountSetting.query.get(1)
    if site is None:
        abort(500)
    blog = Post.query.filter_by(slag=slag, status=True).first_or_404()
    tags = Tag.query.all()
    categories = Category.query.all()
    posttags = PostTag.query.all()
    postcategories = PostCategory.query.all()
    url=None
    if blog.youtube:
        youtube = blog.youtube.replace('watch?v=', 'embed/')
        youtube = youtube.split('/')
        url = f'{ youtube[0] }//{ youtube[2] }/{ youtube[3] }/{ youtube[4] }?autoplay=1&playlist={ youtube[4] }&loop=1'
    return render_template('user/blog.html', title=title, site=site, blog=blog, tags=tags, categories=categories, posttags=posttags, postcategories=postcategories, youtube=url)


#Subscribe Page Route
@user.route('/subscribe', methods=['POST'])
def subscribe():
    if request.form.get('email'):
        if Subscriber.query.filter_by(email=request.form.get('email')).first():
            flash('Already Subscribed', 'subscribe')
        else:
            sub = Subscriber(email=request.form.get('email'))
            db.session.add(sub)
            db.session.commit()
            flash('Successfully Subcribed', 'subscribe')
    else:
        flash('Email field is required', 'subscribe')
    email = request.form.get('email')
    return redirect(request.referrer)


#Search Page Route
@user.route('/search')
def search():
    title = 'SacheFacts | Search'
    site = AccountSetting.query.get(1)
    if site is None:
        abort(500)
    featured = Post.query.filter_by(featured=True, status=True).all()
    blogs = []
    if request.args.get('q'):
        query = f'%{ request.args.get("q").strip() }%'
        blogs = Post.query.filter(Post.title.like(query)).all()
    print(blogs)
    return render_template('user/search.html', title=title, site=site, featured=featured, blogs=blogs)
