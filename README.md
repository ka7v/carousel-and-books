# Carousel__Books
We are developed a book project where used [flask](https://flask.palletsprojects.com/en/2.2.x/), scrap, SQLAlchemy, html, css, bootstrap,

* this is our __book__ project where you can learn new books, share books and discuss, you can leave your comments
* applications written in flask
  * 
      admin panel supports [flask-admin](https://flask-admin.readthedocs.io/en/latest/) and [flask-security](https://pythonhosted.org/Flask-Security/)
      authorization supports [flask-login](https://flask-login.readthedocs.io/en/latest/)
      for the parser we used [requests](https://requests.readthedocs.io/en/latest/) and [bs4](https://beautiful-soup-4.readthedocs.io/en/latest/)
      for data storage we used [sqlite](https://www.sqlite.org/docs.html) and [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

### to use the app, first install the required dependencies, then include the database, then run model.py to create the tables, then run bookinist.py to populate the tables, then run the main.py app.
#### before creating tables, comment the admin part in __init__.py