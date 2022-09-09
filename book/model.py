import collections
from datetime import datetime
from book import db, login_manager
from flask_security import RoleMixin
from flask_login import UserMixin
import email_validator

user_books = db.Table('user_books',
                     db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     extend_existing = True
                     )


# user_role = db.Table('user_roles',
#                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                      db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
#                      extend_existing = True
#                      )

# user_like = db.Table('user_like',
#                      db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
#                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                      db.Column('like_id', db.Integer, db.ForeignKey('like.id'), primary_key=True),
#                      extend_existing = True
#                      )

# user_comment = db.Table('user_comment',
#                      db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
#                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                      db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True),
#                      extend_existing = True
#                      )


def delete_book(book_id):
    book = Books.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()



class Books(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())#.strftime("%m/%d/%Y, %H:%M"))
    genre = db.relationship('Genres', backref='books', lazy='dynamic')
    auther = db.relationship('Auther', backref='books', lazy='dynamic')
    language = db.relationship('Language', backref='books', lazy='dynamic')
    likes = db.relationship('Like', backref='books', lazy='dynamic')
    comment = db.relationship('Comment', backref='books', lazy='dynamic')
    user_book = db.relationship('User', secondary=user_books, cascade="all,delete", backref='books')
    # user_comment = db.relationship('Comment', secondary=user_comment, backref='books', cascade="all,delete")
    # user_like = db.relationship('Like', secondary=user_like, backref='books', cascade="all,delete")


    def __repr__(self):
        return f'{self.date}, {self.photo}, {self.description}, {self.page_count}, {self.name}'

class Genres(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __repr__(self):
        return f'{self.genre}'


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    nick_name = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=True, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    role = db.relationship('Role', backref='user', lazy='dynamic')
    # user_like = db.relationship('Like', secondary=user_like, cascade="all,delete", backref='user')
    # user_comment = db.relationship('Comment', secondary=user_comment, cascade="all,delete", backref='user')

    def __repr__(self):
        return f'{self.last_name}, {self.first_name}, {self.nick_name}, {self.password}, {self.email}'


class Auther(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class Language(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __repr__(self):
        return f'{self.language}'


class Like(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False )
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete="CASCADE"), nullable=False)



def like_count(book_id):
    likes = Like.query.filter_by(book_id=book_id).all()
    count = []
    count1 = 1
    for i in likes:
        count.append(count1)
    l = collections.Counter(count)
    return l[1]


class Comment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    comm = db.Column(db.String(500), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete="CASCADE"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    def __repr__(self):
        return f'{self.comm}'

class Role(db.Model, RoleMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)



@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return User.query.get(user_id)

if __name__ == '__main__':
    db.create_all()


