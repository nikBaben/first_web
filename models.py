from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class Goga(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Otziv(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    bode = db.Column(db.String(50),nullable=False)
    athor = db.Column(db.Integer, db.ForeignKey('goga.id'))
    created_at = db.Column(db.DateTime(True), nullable=False, server_default=db.func.now(tz='UTC'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime(True), nullable=False, server_default=db.func.now(tz='UTC'))
    author_id = db.Column(db.Integer, db.ForeignKey('goga.id'))
    address = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer,nullable=False)
    img = db.Column(db.String(140),nullable=False)

    author = db.relationship('Goga', backref=db.backref('articles', lazy=True))
    category = db.relationship('Category', backref=db.backref('articles', lazy=True))
