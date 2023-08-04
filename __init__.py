# main.py
from flask import Flask, render_template
from flask_mysqldb import MySQL
from .auth import auth

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gsdffsbd bfdbfbfd'

    # Configure MySQL settings
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'trial'

    mysql.init_app(app)

    app.register_blueprint(auth, url_prefix='/')

    return app


app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

# ... Other routes and views ...

if __name__ == '__main__':
    app.run(debug=True)


 