from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import DataManager
from models import db, User, Subscription
from werkzeug.security import generate_password_hash, check_password_hash
import os
from auth import login_required


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
@login_required
def dashboard():
    user_id = session['user_id']
    subs = data_manager.get_subscriptions_by_user(user_id)

    total_monthly_cost = 0
    annual_cost = 0
    categories = {}

    for s in subs:
        if s.billing_cycle == "Monthly":
            total_monthly_cost += s.price
            annual_cost += s.price * 12
        elif s.billing_cycle == "Yearly":
            total_monthly_cost += s.price / 12
            annual_cost += s.price

        categories[s.category] = categories.get(s.category, 0) + 1

    # Top category
    top_category = None
    if categories:
        top_category = max(categories, key=categories.get)

    return render_template(
        "dashboard.html",
        total_monthly_cost=round(total_monthly_cost, 2),
        annual_cost=round(annual_cost, 2),
        sub_count=len(subs),
        subs=subs,
        categories=categories,
        top_category=top_category
    )


@app.route('/subscriptions', methods=['GET', 'POST'])
@login_required
def subscriptions():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        billing_cycle = request.form.get('billing_cycle')
        next_payment_date = request.form.get('next_payment_date')
        category = request.form.get('category')

        user_id = session['user_id']
        data_manager.add_subscription(
            name, price, billing_cycle, next_payment_date, category, user_id
        )
        return redirect(url_for('subscriptions'))

    user_id = session['user_id']
    subs = data_manager.get_subscriptions_by_user(user_id)
    return render_template('subscriptions.html', subs=subs)


@app.route('/subscriptions/<int:sub_id>/delete', methods=['POST'])
@login_required
def delete_subscription(sub_id):
    data_manager.delete_subscription(sub_id)
    return redirect(url_for('subscriptions'))


@app.route('/subscriptions/<int:sub_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subscription(sub_id):
    sub = data_manager.get_subscription_by_id(sub_id)

    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        billing_cycle = request.form.get('billing_cycle')
        next_payment_date = request.form.get('next_payment_date')
        category = request.form.get('category')

        data_manager.update_subscription(
            sub_id, name, price, billing_cycle, next_payment_date, category
        )
        return redirect(url_for('subscriptions'))

    return render_template('edit_subscription.html', sub=sub)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)