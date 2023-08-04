from flask import Blueprint, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

auth = Blueprint("auth", __name__)
mysql = MySQL()

# Configure MySQL settings
auth.config = {
    'MYSQL_HOST': 'localhost',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': 'root', 
    'MYSQL_DB': 'trial',
}

mysql.init_app(auth)

# ... (previous code remains the same)

@auth.route('/', methods=['GET', 'POST'])
def login_signup():
    if request.method == 'POST':
        form_type = request.form.get('form-type')

        if form_type == 'login':
            email = request.form.get('email')
            password = request.form.get('password')
            print("User entered email:", email)
            print("User entered password:", password)

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            cur.close()

            if user_data:
                # Convert tuple to a dictionary (with column names as keys)
                user = {
                    'name': user_data[0],
                    'email': user_data[1],
                    'password': user_data[2]
                }

                if sha256_crypt.verify(password, user['password']):
                    # Successful login: Redirect to the dashboard
                    return redirect(url_for('auth.dashboard', email=email))
                else:
                    print("Invalid email or password.")
                    print("User from the database:", user)
                    return render_template("index.html", error_message='Invalid email or password. Please try again.')
            else:
                print("User not found.")
                return render_template("index.html", error_message='User not found.')

        # ... (signup section and other code remains the same)

# ... (remaining code remains the same)


        elif form_type == 'signup':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            print("User entered name:", name)
            print("User entered email:", email)
            print("User entered password:", password)

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            cur.close()

            print("Existing user from the database:", existing_user)

            if existing_user:
                print("An account with this email already exists. Please log in.")
                return render_template("index.html", error_message='An account with this email already exists. Please log in.')

            # Hash the password before storing it in the database
            hashed_password = sha256_crypt.hash(password)

            # Insert new user data into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('auth.dashboard', email=email))

    return render_template('index.html')


@auth.route('/dashboard/<string:email>')
def dashboard(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('auth.login_signup'))

# Add more routes and functions as needed...

# End of auth.py
