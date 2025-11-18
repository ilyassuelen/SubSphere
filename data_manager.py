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

    def get_subscriptions_by_user(self, user_id):
        return Subscription.query.filter_by(user_id=user_id).all()

    def get_monthly_total(self, user_id):
        subs = self.get_subscriptions_by_user(user_id)
        total = 0
        for s in subs:
            if s.billing_cycle == "Monthly":
                total += s.price
            elif s.billing_cycle == "Yearly":
                total += s.price / 12
        return round(total, 2)

    def count_subscriptions(self, user_id):
        return Subscription.query.filter_by(user_id=user_id).count()

    def delete_subscription(self, sub_id):
        sub = Subscription.query.get(sub_id)
        db.session.delete(sub)
        db.session.commit()

    def get_subscription_by_id(self, sub_id):
        return Subscription.query.get(sub_id)

    def update_subscription(self, sub_id, name, price, billing_cycle, next_payment_date, category):
        sub = Subscription.query.get(sub_id)
        sub.name = name
        sub.price = price
        sub.billing_cycle = billing_cycle
        sub.next_payment_date = datetime.strptime(next_payment_date, "%Y-%m-%d")
        sub.category = category
        db.session.commit()
