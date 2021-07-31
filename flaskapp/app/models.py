# This contains all the database elements of the application
# Extension for implementing SQLAlchemy ORM
from sqlalchemy import event
# Extension for implementing Flask-Login for authentication
from flask_login import UserMixin
# Methods from Werkzeug for managing password hashing and sanitizing filenames
from werkzeug.security import generate_password_hash, check_password_hash
# Package for creating slugs
from slugify import slugify
# Methods for generating tokens
from secrets import token_urlsafe
# Imports from the app package
from app import db, login_manager


# Album SQLAlchemy model
class unit1(db.Model):
    __tablename__ = "unit1"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text(), nullable=False)
    release_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), index=True, nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title, artist, description, genre, image, release_date, user_id):
        self.title = title
        self.artist = artist
        self.description = description
        self.genre = genre
        self.image = image
        self.release_date = release_date
        self.user_id = user_id


# Tour SQLAlchemy model
class unit2(db.Model):
    __tablename__ = "unit2"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), index=True, nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title, artist, description, genre, start_date, end_date, user_id):
        self.title = title
        self.artist = artist
        self.description = description
        self.genre = genre
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id


# Method for updating slugs on title update
def update_slug(target, value, old_value, initiator):
    target.slug = slugify(value) + "-" + token_urlsafe(3)


event.listen(unit1.title, "set", update_slug)
event.listen(unit2.title, "set", update_slug)


# User SQLAlchemy model
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    albums = db.relationship("unit1", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    tours = db.relationship("unit2", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, username="", email="", password=""):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "<User %r>" % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_album_owner(self, unit1):
        return self.id == unit1.user_id

    def is_tour_owner(self, unit2):
        return self.id == unit2.user_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
