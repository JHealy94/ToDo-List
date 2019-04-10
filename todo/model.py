from datetime import datetime
from todo import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    lists = db.relationship('List', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}"


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('ListItem', backref='list', lazy=True)

    def __repr__(self):
        return f"List('{self.title}', {self.date_posted}')"


class ListItem(db.Model):
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key=True, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(160), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Item ('{self.list_id}', '{self.date_added}')"
