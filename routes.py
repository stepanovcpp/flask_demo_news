from flask import render_template, request, redirect, session

from database import db
from hashpass import hash_password, verify_password
from models.Article import Article
from models.User import User
from Config import Config
from werkzeug.utils import secure_filename
import os
import os.path as path


conf = Config()

# not route functions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in conf.ALLOWED_EXTENSIONS


def get_unique_filename(upload_folder, original_filename):
    filename = secure_filename(original_filename)

    base, ext = os.path.splitext(filename)

    counter = 1

    unique_filename = filename

    while os.path.exists(os.path.join(upload_folder, unique_filename)):
        unique_filename = f"{base}({counter}){ext}"
        counter += 1

    return unique_filename


def delete_file_by_name(folder_path, filename):
    full_path = path.join(folder_path, filename)
    if path.isfile(full_path):
        try:
            os.remove(full_path)
            return True
        except OSError as e:
            return False

    return True


# route functions


def index():
    articles = Article.query.all()
    articles.reverse()
    all_users = db.session.execute(db.select(User)).scalars().all()
    users_dict = {user.id: user for user in all_users}
    return render_template('news.html', session=session, articles=articles, users=users_dict)


def registration():
    if request.method == 'GET':
        return render_template('registration.html')

    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')

    if not fullname or not email or not password:
        return redirect('/registration')

    check_in_db_by_email = User.query.filter_by(email=email).first()
    check_in_db_by_fullname = User.query.filter_by(full_name=fullname).first()

    if check_in_db_by_email or check_in_db_by_fullname:
        return redirect('/registration')

    hashed_password = hash_password(password)

    user = User(full_name=fullname, email=email, password_hash=hashed_password)

    try:
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    except:
        return redirect('/registration')


def login():
    if session.get('logged_in'):
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return redirect('/login')

    check_in_db_by_email = User.query.filter_by(email=email).first()

    if check_in_db_by_email is None or not verify_password(password, check_in_db_by_email.password_hash):
        return redirect('/login')

    session['logged_in'] = True
    session['user_id'] = check_in_db_by_email.id
    session['email'] = check_in_db_by_email.email
    session['fullname'] = check_in_db_by_email.full_name
    session['count_of_posts'] = check_in_db_by_email.count_of_posts

    return redirect('/')

def logout():
    session.clear()
    return redirect('/')

def create_post(upload_folder):
    if not session.get('logged_in'):
        return redirect('/')

    if request.method == 'GET':
        return render_template('create_post.html', session=session)

    title = request.form.get('title')
    intro = request.form.get('intro')
    content = request.form.get('content')
    file = request.files['file']

    if not title or not intro or not content or not file.filename:
        return redirect('/create_post')

    if file and allowed_file(file.filename):
        filename = get_unique_filename(upload_folder, file.filename)
        file.save(os.path.join(upload_folder, filename))

        article = Article(title=title, intro=intro, content=content, image=filename, user_id=session.get('user_id'))

        user = db.session.get(User, session.get('user_id'))

        try:
            db.session.add(article)
            user.count_of_posts += 1
            session['count_of_posts'] = user.count_of_posts
            db.session.commit()
            return redirect('/post/' + str(article.id))
        except:
            return redirect('/create_post')

    return redirect('/create_post')


def post(id):
    article = Article.query.get(id)
    all_users = db.session.execute(db.select(User)).scalars().all()
    users_dict = {user.id: user for user in all_users}
    return render_template('post.html', session=session, article=article, users=users_dict)


def profile():
    if not session.get('logged_in'):
        return redirect('/')

    articles = Article.query.filter_by(user_id=session.get('user_id')).all()
    articles.reverse()
    all_users = db.session.execute(db.select(User)).scalars().all()
    users_dict = {user.id: user for user in all_users}
    return render_template('profile.html', session=session, articles=articles, users=users_dict)


def udate_post(id, upload_folder):
    if not session.get('logged_in'):
        return redirect('/')

    article = Article.query.get(id)

    if article.user_id != session.get('user_id'):
        return redirect('/')

    if request.method == 'GET':
        return render_template('update_post.html', session=session, article=article)


    title = request.form.get('title')
    intro = request.form.get('intro')
    content = request.form.get('content')
    file = request.files['file']

    if not title or not intro or not content:
        return redirect('/update_post/' + str(id))

    if file and allowed_file(file.filename):
        filename = get_unique_filename(upload_folder, file.filename)
        file.save(os.path.join(upload_folder, filename))

        delete_file_by_name(upload_folder, article.image)

        article.image = filename

    article.title = title
    article.intro = intro
    article.content = content

    try:
        db.session.commit()
        return redirect('/post/' + str(id))
    except:
        return redirect('/update_post/' + str(id))


def delete_post(id, upload_folder):
    if not session.get('logged_in'):
        return redirect('/')

    article = Article.query.get(id)

    if article.user_id != session.get('user_id'):
        return redirect('/')

    user = db.session.get(User, session.get('user_id'))

    try:
        db.session.delete(article)
        delete_file_by_name(upload_folder, article.image)
        user.count_of_posts -= 1
        session['count_of_posts'] = user.count_of_posts
        db.session.commit()
        return redirect('/')
    except:
        return redirect('/post/' + str(id))


def about():
    return render_template('about.html', session=session)
