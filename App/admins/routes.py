from App import bcrypt, db, app
from App.admins import admin
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from App.admins.forms import LoginForm, TagForm, DeleteForm, CategoryForm, PostCreateForm, AccountForm, PasswordForgetForm, ProfileLoginForm, PasswordResetForm
from App.models import Admin, Post, Tag, Category, PostTag, PostCategory, PostImage, AccountSetting
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import shutil


def fileupload(file, folder, thumbnail=False):
    path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    if thumbnail:
        ext = os.path.splitext(file.filename)[1][1:].strip()
        file.filename = f'thumbnail_{ folder }.{ ext }'
    filename = secure_filename(file.filename).lower()
    file.save(os.path.join(path, filename))
    return f'{ folder }/{ filename }'



def filedelete(file, folder=False):
    path = os.path.join(app.config['UPLOAD_FOLDER'], file)
    if os.path.exists(path):
        if folder:
            shutil.rmtree(path)
        else:
            os.remove(path)
    return


def siteupload(file):
    filename = secure_filename(file.filename).lower()
    file.save(os.path.join(app.config['UPLOAD_SITE'], filename))
    return f'site/{ filename }'


def tagcategory(obj, name):
    val = obj.query.filter_by(name=name).first()
    if val:
        return str(val.id)
    else:
        addval=obj(name=name.upper())
        db.session.add(addval)
        db.session.commit()
        return tagcategory(obj, name)


#Login Page Routes
@admin.route('/wp-login' ,methods=['GET', 'POST'])
def login():
    nexturl = request.args.get('next')
    if current_user.is_authenticated:
        return redirect(url_for('admins.home'))
    else:
        title = 'Sache Fact | Login'
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            admin = Admin.query.filter_by(username=request.form.get('username')).first()
            if admin and bcrypt.check_password_hash(admin.password, request.form.get('password')):
                login_user(admin)
                flash('Login successfull', 'success')
                return redirect(nexturl or url_for('admins.home'))
            else:
                flash('Wrong Login Credentials', 'danger')
        return render_template('admin/login.html', title=title, form=form)


#Logout Routes
@admin.route('/wp-login/logout')
def logout():
    logout_user()
    return redirect(url_for('users.home'))


#DashBoard Page Routes
@admin.route('/wp-admin')
@admin.route('/wp-admin/home')
@admin.route('/wp-admin/dashboard')
@login_required
def home():
    title = 'Sache Fact'
    data = []
    data.append(Post.query.count())
    data.append(Tag.query.count())
    data.append(Category.query.count())
    data.append(PostImage.query.count())
    return render_template('admin/home.html', title=title, data=data)


#Tag Page Routes
@admin.route('/wp-admin/tag', methods=['GET', 'POST'])
@login_required
def tag():
    title = 'Sache Fact | Tags'
    form = TagForm()
    formDelete = DeleteForm()
    tags = Tag.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        tag = Tag(name=request.form.get('name').upper())
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('admins.tag'))
    return render_template('admin/tag.html', title=title, form=form, formDelete=formDelete, tags=tags)


#Tag Delete Routes
@admin.route('/wp-admin/tagdelete', methods=['POST'])
@login_required
def deletetag():  
    title = 'Sache Fact | Tags'
    if request.method == 'POST':
        print(request.form)
        Tag.query.filter_by(id=request.form.get('deleteid')).delete()
        PostTag.query.filter_by(post_id=request.form.get('deleteid')).delete()
        db.session.commit()
    return redirect(url_for('admins.tag'))


#Category Page Routes
@admin.route('/wp-admin/category', methods=['GET', 'POST'])
@login_required
def category():
    title = 'Sache Fact | Categories'
    form = CategoryForm()
    formDelete = DeleteForm()
    categories = Category.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(name=request.form.get('name').upper())
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admins.category'))
    return render_template('admin/category.html', title=title, form=form, formDelete=formDelete, categories=categories)


#Category Delete Routes
@admin.route('/wp-admin/categorydelete', methods=['POST'])
@login_required
def deletecategory():  
    title = 'Sache Fact | Categories'
    if request.method == 'POST':
        category.query.filter_by(id=request.form.get('deleteid')).delete()
        PostCategory.query.filter_by(post_id=request.form.get('deleteid')).delete()
        db.session.commit()
    return redirect(url_for('admins.category'))


#Post Create Page Routes
@admin.route('/wp-admin/blog/create', methods=['GET', 'POST'])
@login_required
def createpost():
    title = 'Sache Fact | Blog'
    form = PostCreateForm()
    tags = Tag.query.all()
    categories = Category.query.all()
    form.selecttag.choices = [(tag.id, tag.name) for tag in tags]
    form.selectcategory.choices = [(category.id, category.name) for category in categories]
    if request.method == 'POST' and form.validate_on_submit():
        heading=request.form.get('title')
        slag = secure_filename(heading).lower()
        thumbnail = fileupload(request.files.get('thumbnail'), slag, True)
        selectcategory=request.form.getlist('selectcategory')
        selecttag=request.form.getlist('selecttag')
        category = request.form.get('category')
        if category:
            categories = list(category.split(','))
            for category in categories:
                id = tagcategory(Category, category)
                selectcategory.append(id)
        tag=request.form.get('tag')
        if tag:
            categories = list(tag.split(','))
            for tag in categories:
                id = tagcategory(Tag, tag)
                selecttag.append(id)
        content=request.form.get('content')
        youtube=request.form.get('youtube')
        facebook=request.form.get('facebook')
        instagram=request.form.get('instagram')
        link1=request.form.get('link1')
        link2=request.form.get('link2')
        featured=False
        if request.form.get('featured'):
            featured=True
        #video=request.form.get('video')
        if len(selectcategory) == 0 and len(category) == 0:
            flash(f'Category is required for post { heading }', 'warning')
        elif len(selecttag) == 0 and len(tag) == 0:
            flash(f'Tag is required for post { heading }', 'warning')
        else:
            post = Post(title=heading, slag=slag, content=content, youtube=youtube, facebook=facebook, instagram=instagram, link1=link1, link2=link2, thumbnail=thumbnail, featured=featured, created_at=datetime.now())
            db.session.add(post)
            db.session.commit()
            for ids in selecttag:
                addtag = PostTag(post_id=post.id, tag_id=ids)
                db.session.add(addtag)
            for ids in selectcategory:
                addcategory = PostCategory(post_id=post.id, category_id=ids)
                db.session.add(addcategory)
            db.session.commit()
            return redirect(url_for('admins.viewpost'))
    return render_template('admin/blog/create.html', title=title, form=form)


#Summernote Image Routes
@admin.route('/wp-admin/summernoteImages', methods=['POST'])
@login_required
def summernote():
    image = fileupload(request.files.get('file'), secure_filename(request.form.get('folder')).lower())
    imglist = list(image.split('/'))
    postimage = PostImage(slag=imglist[0], image=imglist[1])
    db.session.add(postimage)
    db.session.commit()
    return f"{ url_for('static', filename=f'post/{ image }') }"


#All Post View Page Routes
@admin.route('/wp-admin/blogs')
@login_required
def viewpost():
    title = 'Sache Fact | Blog'
    posts = Post.query.all()
    form = DeleteForm()
    return render_template('admin/blog/viewall.html', title=title, posts=posts, formDelete=form)


#Status Featured Routes
@admin.route('/wp-admin/featuredstatus')
@login_required
def featuredstatus():
    post = Post.query.get(request.args.get('id'))
    if request.args.get('type') == 'status':
        post.status = not(post.status)
    elif request.args.get('type') == 'featured':
        post.featured = not(post.featured)
    else:
        pass
    db.session.commit()
    return redirect(url_for('admins.viewpost'))


#Status Featured Routes
@admin.route('/wp-admin/blog/delete', methods=['POST'])
@login_required
def deletepost():
    if request.form.get('deleteid'):
        try:
            post = Post.query.filter_by(id=request.form.get('deleteid')).first()
            filedelete(post.slag, True)
            PostCategory.query.filter_by(post_id=request.form.get('deleteid')).delete()
            PostTag.query.filter_by(post_id=request.form.get('deleteid')).delete()
            PostImage.query.filter_by(slag=post.slag).delete()
            Post.query.filter_by(id=request.form.get('deleteid')).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    return redirect(url_for("admins.viewpost"))


#Post View Page Routes
@admin.route('/wp-admin/blog/<slag>')
@login_required
def viewsinglepost(slag):
    title = 'Sache Fact | Blog'
    tags = []
    categories = []
    post = Post.query.filter_by(slag=slag).first_or_404()
    posttags = PostTag.query.filter_by(post_id=post.id).all()
    for posttag in posttags:
        tag = Tag.query.get(posttag.tag_id)
        tags.append(tag.name)
    postcategories = PostCategory.query.filter_by(post_id=post.id).all()
    for postcategory in postcategories:
        category = Category.query.get(postcategory.category_id)
        categories.append(category.name)
    return render_template('admin/blog/view.html', title=title, post=post, tags=tags, categories=categories)


#Post View Page Routes
@admin.route('/wp-admin/blog/<slag>/edit', methods=['GET', 'POST'])
@login_required
def editpost(slag):
    taglist = []
    categorylist = []
    title = 'Sache Fact | Blog'
    post = Post.query.filter_by(slag=slag).first_or_404()
    form = PostCreateForm(obj=post)
    if request.method == 'POST':
        if request.form.get('content'):
            post.content = request.form.get('content')
        if request.form.get('youtube'):
            post.youtube = request.form.get('youtube')
        if request.form.get('facebook'):
            post.facebook = request.form.get('facebook')
        if request.form.get('instagram'):
            post.instagram = request.form.get('instagram')
        if request.form.get('link1'):
            post.link1 = request.form.get('link1')
        if request.form.get('link2'):
            post.link2 = request.form.get('link2')
        if request.form.get('featured'):
            post.featured = True
        else:
            post.featured = False
        if request.files.get('thumbnail') and request.form.get('title'):
            oldpic = post.thumbnail
            newpic = fileupload(request.files.get('thumbnail'), secure_filename(request.form.get('title')).lower(), True)
            post.thumbnail = newpic
            if newpic != oldpic:
                filedelete(oldpic)
        PostCategory.query.filter_by(post_id=post.id).delete()
        PostTag.query.filter_by(post_id=post.id).delete()
        if request.form.get('category'):
            selectcategory = request.form.getlist('selectcategory')
            if request.form.get('category'):
                categories = list(request.form.get('category').split(','))
                for category in categories:
                    id = tagcategory(Category, category)
                    selectcategory.append(id)
            for ids in selectcategory:
                addcategory = PostCategory(post_id=post.id, category_id=ids)
                db.session.add(addcategory)
        if request.form.get('tag'):
            selecttag = request.form.getlist('selecttag')
            if request.form.get('tag'):
                tags = list(request.form.get('tag').split(','))
                for tag in tags:
                    id = tagcategory(Tag, tag)
                    selecttag.append(id)
            if len(selecttag) > 0:
                for ids in selecttag:
                    addtag = PostTag(post_id=post.id, tag_id=ids)
                    db.session.add(addtag)
        db.session.commit()
        return redirect(url_for('admins.viewsinglepost', slag=slag))
    posttag = PostTag.query.filter_by(post_id=post.id).all()
    for pt in posttag:
        tag = Tag.query.get(pt.tag_id)
        taglist.append(tag.name)
    postcategory = PostCategory.query.filter_by(post_id=post.id).all()
    for pc in postcategory:
        category = Category.query.get(pc.category_id)
        categorylist.append(category.name)
    categorystr = ','.join(map(str, categorylist))
    tagstr = ','.join(map(str,taglist))
    tags = Tag.query.all()
    categories = Category.query.all()
    form.selecttag.choices = [(tag.id, tag.name) for tag in tags]
    form.selectcategory.choices = [(category.id, category.name) for category in categories]
    form.category.data = categorystr
    form.tag.data = tagstr
    form.title.render_kw = {'readonly':True}
    return render_template('admin/blog/edit.html', title=title, form=form, slag=post.slag, thumbnail=post.thumbnail)


#Images View Page Routes
@admin.route('/wp-admin/media')
@login_required
def media():
    if request.args.get('page'):
        if int(request.args.get('page')) > 0:
            page = int(request.args.get('page'))
        else:
            abort(404)
    else:
        page=1
    per_page=12
    title = 'Sache Fact | Media'
    form = DeleteForm()
    images = PostImage.query.paginate(page, per_page)
    return render_template('admin/media.html', title=title, images=images, formDelete=form)


#Images Delete Page Routes
@admin.route('/wp-admin/media/delete', methods=['POST'])
@login_required
def deletemedia():
    if request.form.get('deleteid'):
        media = PostImage.query.get_or_404(request.form.get('deleteid'))
        file=f'{ media.slag }/{ media.image }'
        print(file)
        filedelete(file)
        PostImage.query.filter_by(id=request.form.get('deleteid')).delete()
        db.session.commit()
    return redirect(url_for("admins.media"))


#Account view Page Routes
@admin.route('/wp-admin/account', methods=['GET', 'POST'])
@login_required
def account():
    title = 'Sache Fact | Account'
    account = AccountSetting.query.get_or_404(1)
    profile = Admin.query.filter_by(id=1, role='admin').first_or_404()
    form = AccountForm(obj=account)
    form2 = ProfileLoginForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            account.site_title = request.form.get('site_title')
            account.site_youtube = request.form.get('site_youtube')
            account.site_facebook = request.form.get('site_facebook')
            account.site_instagram = request.form.get('site_instagram')
            account.admin_firstname = request.form.get('admin_firstname')
            account.admin_lastname = request.form.get('admin_lastname')
            account.admin_displayname = request.form.get('admin_displayname')
            account.admin_contact = request.form.get('admin_contact')
            account.admin_email = request.form.get('admin_email')
            account.admin_address = request.form.get('admin_address')
            if request.files.get('site_logo'):
                oldpic = account.site_logo
                newpic = siteupload(request.files.get('site_logo'))
                account.site_logo = newpic
                if newpic != oldpic:
                    filedelete(oldpic)
            if request.files.get('site_poster'):
                oldpic = account.site_poster
                newpic = siteupload(request.files.get('site_poster'))
                account.site_poster = newpic
                if newpic != oldpic:
                    filedelete(oldpic)
            if request.files.get('admin_photo'):
                oldpic = account.admin_photo
                newpic = siteupload(request.files.get('admin_photo'))
                print(newpic)
                account.admin_photo = newpic
                if newpic != oldpic:
                    filedelete(oldpic)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return redirect(url_for('admins.account'))
    form2.key.data = profile.email
    return render_template('admin/account.html', title=title, form=form, sl=account.site_logo, sp=account.site_poster, ap=account.admin_photo, form2=form2, key=bcrypt.generate_password_hash(profile.email).decode('utf-8'))


#Password Forget route
@admin.route('/wp-admin/account/login-update', methods=['POST'])
def loginupdate():
    title = 'Sache Facts - Login Update'
    form = ProfileLoginForm()
    profile = Admin.query.filter_by(id=1, role='admin').first_or_404()
    if request.method == 'POST' and form.validate_on_submit():
        if bcrypt.check_password_hash(request.args.get('key'), request.form.get('key')):
            try:
                if request.form.get('username'):
                    profile.username = request.form.get('username')
                if request.form.get('email'):
                    profile.email = request.form.get('email')
                if request.form.get('password'):
                    profile.password = request.form.get('password')
                db.session.commit()
                return redirect(url_for('admins.logout'))
            except Exception as e:
                print(e)
                db.session.rollback()
    return redirect(url_for('admins.account'))


#Password Forget route
@admin.route('/wp-password-forget', methods=['GET', 'POST'])
def passwordforget():
    title = 'Sache Facts - Password Forget'
    form = PasswordForgetForm()
    if request.method == 'POST' and form.validate_on_submit():
        profile = Admin.query.filter_by(email=request.form.get('email')).first();
        if profile:
            link = f"{ url_for('admins.passwordreset', id=profile.role, hid=bcrypt.generate_password_hash(profile.role).decode('utf-8'), email=profile.email, hemail=bcrypt.generate_password_hash(profile.email).decode('utf-8')) }"
            print(link)
            flash('Password reset link is sent to registered Email id', 'success')
        else:
            flash('Wrong Email..!!', 'danger')
        return redirect(url_for('admins.login'))
    return render_template('admin/password/forget.html', title=title, form=form)


#Password Recovery route
@admin.route('/wp-password-reset', methods=['GET', 'POST'])
def passwordreset():
    title = 'Sache Facts - Password Reset'
    if request.args.get('hid') and request.args.get('id') and request.args.get('hemail') and request.args.get('email'):
        if bcrypt.check_password_hash(request.args.get('hid'), request.args.get('id')) and bcrypt.check_password_hash(request.args.get('hemail'), request.args.get('email')):
            profile = Admin.query.filter_by(role=request.args.get('id'), email=request.args.get('email')).first_or_404()
            form = PasswordResetForm()
            if request.method == 'POST' and form.validate_on_submit():
                profile.password = request.form.get('password')
                db.session.commit()
                flash('Password successfully reset', 'success')
                return redirect(url_for('admins.login'))
            return render_template('admin/password/reset.html', title=title, form=form)
    return redirect(url_for('admins.login'))
