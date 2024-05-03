from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroup.id'))
    year = db.relationship('Year', backref=db.backref('users', lazy=True))
    department = db.relationship('Department', backref=db.backref('users', lazy=True))
    subgroup = db.relationship('Subgroup', backref=db.backref('users', lazy=True))

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)


class Hostel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostel_id = db.Column(db.Integer, db.ForeignKey(
        'hostel.id'), nullable=False)
    hostel = db.relationship('Hostel', backref=db.backref('menus', lazy=True))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    day = db.relationship('Day', backref=db.backref('menus', lazy=True))


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    menu = db.relationship('Menu', backref=db.backref('menu_items', lazy=True))
    meal = db.Column(db.String(20), nullable=False)  # Breakfast, Lunch, Dinner
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Subgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    day = db.relationship('Day', backref=db.backref('timetable', lazy=True))
    time = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), nullable=False)
    subgroup_id = db.Column(db.Integer, db.ForeignKey(
        'subgroup.id'), nullable=False)
