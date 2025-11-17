from models import db, User, Subscription
from datetime import datetime

class DataManager:
    def create_user(self, name, email, password_hash):
        new_user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def add_subscription(self, name, price, billing_cycle, next_payment_date, category, user_id):
        new_subscription = Subscription(
            name=name,
            price=price,
            billing_cycle=billing_cycle,
            next_payment_date=datetime.strptime(next_payment_date, "%Y-%m-%d"),
            category=category,
            user_id=user_id
        )

        db.session.add(new_subscription)
        db.session.commit()
        return new_subscription