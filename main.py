from book import app
from book import views
from book.posts.blueprint import posts


if __name__ == '__main__':
    app.register_blueprint(posts, url_prefix='/posts')
    app.run()
