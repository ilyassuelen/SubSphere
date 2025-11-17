from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import DataManager
from models import db, User, Subscription
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.secret_key = "super-secret-key-change-later"

# Configuring SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/subs.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect DB & App
db.init_app(app)

# Create DataManager Object
data_manager = DataManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        mail_exists = data_manager.get_user_by_email(email)
        if mail_exists:
            return render_template('register.html', error="Email already registered")

        hashed_pw = generate_password_hash(password)
        user = data_manager.create_user(name, email, hashed_pw)

        session['user_id'] = user.id
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = data_manager.get_user_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            return render_template('login.html', error="Invalid email or password")

        session['user_id'] = user.id
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template("dashboard.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)