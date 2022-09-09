from flask import Flask, url_for, redirect
from book.config import configuration
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(configuration)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user'



from book.model import User, Role, Books

class AdminMixin:
    def is_accessible(self):
        admin = User.query.get(1)
        return current_user == admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect( url_for('posts.profile'))

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'Admin', url='/', index_view=HomeAdminView(name='home'))
admin.add_view(AdminView(Books, db.session))
admin.add_view(AdminView(User, db.session))





