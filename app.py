from flask import Flask, render_template
from models import db, User, Subscription
import os


app = Flask(__name__)

# Configuring SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/subs.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect DB & App
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)