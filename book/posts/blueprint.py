from flask import Blueprint, render_template, flash, redirect, url_for, request
from book.config import configuration
from flask_login import logout_user, current_user, login_required
from book import db
from book.model import Books, Genres, Auther, Language, User, Like, Comment, Role, like_count

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/')
@login_required
def profile():
    id = current_user
    User_books = id.books
    if User_books:
        lang = Language
        auth = Auther
        genre = Genres
        like = like_count
        comment = Comment

        return render_template('profile.html', title='profile', books=User_books, language=lang, auther=auth, genre=genre, comment=comment, like_count=like)
    return render_template('profile.html', title='profile')

@posts.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you are logout", "success")
    return redirect(url_for('home'))

@posts.route('/add_book', methods=['POST', 'GET'])
@login_required
def add_book():
    if request.method == 'POST':
        name = request.form.get('name')
        genre = request.form.get('genre')
        author = request.form.get('author')
        description = request.form.get('description')
        page_count = request.form.get('page')
        page_count = int(page_count)
        language = request.form.get('language')
        im = 'images/standart.jpg'
        book = Books(name=name, description=description, photo=f'{im}', page_count=page_count)
        book.user_book.append(current_user)
        db.session.add(book)
        db.session.commit()
        book_genre = Genres(genre=genre, book_id=book.id)
        db.session.add(book_genre)
        db.session.commit()
        if author:
            book_auther = Auther(name=author, book_id=book.id)
        else:
            book_auther = Auther(name='auther -', book_id=book.id)
        db.session.add(book_auther)
        db.session.commit()
        if language:
            book_language = Language(language=language, book_id=book.id)
        else:
            book_language = Language(language="language -", book_id=book.id)
        db.session.add(book_language)
        db.session.commit()
        book.user_book.append(current_user)
        db.session.commit()
        flash("book added successfully", category="successful")
        return redirect(url_for('posts.profile'))
    return render_template('add_book.html', title='add book')


@posts.route('/like', methods=['POST', 'GET'])
@login_required
def like():
    if request.method == 'POST':
        book_id = request.form['likes']
        like = Like.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if not like:
            like = Like(user_id=current_user.id, book_id=book_id)
            db.session.add(like)
            db.session.commit()
        else:
            db.session.delete(like)
            db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))


@posts.route('/comment', methods=['POST'])
@login_required
def comment():
    if request.method == 'POST':
        comm = request.form['comm']
        book_id = request.form['id']
        user_com = Comment(comm=comm, book_id=book_id, user_id=current_user.id)
        db.session.add(user_com)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))
