from werkzeug.security import generate_password_hash, check_password_hash
from book import app
from flask import render_template, request, redirect, flash, url_for
from .model import db, Role
from .model import Books, User, Language, Auther, Comment, Genres, like_count
import re
from flask_login import login_user, current_user


@app.route("/")
def home():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        try:
            search = Books.query.filter(Books.name.contains(q))
            print(search)
            lang = Language
            auth = Auther
            genre = Genres
            pages = search.paginate(page=page, per_page=4)
            comment = Comment
            return render_template('home.html', book=search, language=lang, auther=auth, pages=pages, genre=genre, title='home', like_count=like_count, comment=comment)
        except Exception as e:
            print(e)
            return redirect(url_for('home'))
    else:
        info = Books.query.order_by(Books.name, Books.id, Books.photo, Books.description, Books.page_count, Books.date)
        lang = Language
        auth = Auther
        genre = Genres
        admin = User.query.get(1)
        pages = info.paginate(page=page, per_page=4)
        comment = Comment
        like = like_count
        return render_template('home.html', books=info, language=lang, auther=auth, genre=genre, title='home', admin=admin,  pages=pages, comment=comment, like_count=like)

# @app.route("/genres")
# def genre():
#     nm = request.form.get('genre')
#     books = Genres.query.filter_by(genre=nm).all()
#     lang = Language
#     auth = Auther
#     genre = Genres
#     comment = Comment
#     return render_template('genres.html', books=books, language=lang, auther=auth, genre=genre, title='genres', like_count=like_count, comment=comment)


@app.route("/user", methods =['GET', 'POST'])
def user():
    if current_user.is_authenticated:
        return redirect(url_for('posts.profile'))
    if request.method == "POST":
        print(request.form['psw'])
        print(request.form['email'])
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, str(request.form['psw'])):
            rm = True if request.form.get('remainme') else False
            login_user(user=user, remember=rm)
            return redirect(request.args.get("next") or url_for('home'))
        flash("not correct login or password")
    return render_template('sign_in.html', title='sign in')


@app.route("/loge in", methods=['GET','POST'])
def loge_in():
    if current_user.is_authenticated:
        return redirect(url_for('posts.profile'))
    if request.method == "POST":
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?).{8,}$"
        email_pattern = r'[^@]+@[^@]+\.[^@]+'
        user_pattern = r'[A-Za-z0-9]+'
        username = request.form['name']
        firstname = request.form['firstname']
        password = request.form['pswd']
        email = request.form['email']
        password2 = request.form['pswd2']
        nickname = request.form['nickname']
        print(password,firstname,nickname, email, username)
        # if not User.query.filter_by(password=password) and User.query.filter_by(user_email=email):
        if not re.match(email_pattern, email):
             flash('Invalid email address !')
        elif not re.match(user_pattern, username):
             flash('Username must contain only characters and numbers !')
        elif not re.match(password_pattern, password):
             flash('ease password')
        elif password != password2:
             flash('passwords are not ecual')
        else:
            hash_pswd = generate_password_hash(password)
            new_user = User(last_name=username, first_name=firstname, nick_name=nickname, password=hash_pswd, email=email)
            print(new_user.email, new_user.password, new_user.nick_name, new_user.first_name, new_user.last_name)
            db.session.add(new_user)
            db.session.commit()
            role = Role(role='user', user_id=new_user.id)
            db.session.add(role)
            db.session.commit()
            return redirect(url_for('home'))
        return redirect(url_for('loge_in'))
    return render_template('registr.html')


@app.errorhandler(404)
def not_page(error):
    return redirect(url_for('home'))
