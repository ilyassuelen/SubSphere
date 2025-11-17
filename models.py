from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscriptions = db.relationship('Subscription', backref='user', lazy=True)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(20), nullable=False)
    next_payment_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
