from models import db, User, Subscription


class DataManager():
    def create_user(self, name, email, password_hash):
        new_user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()