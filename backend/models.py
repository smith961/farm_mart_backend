from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db

"""
class User():
  ADMIN = 'admin'
  FARMER = 'farmer'
  USER = 'user'
"""

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column("password", db.String(128), nullable=False)
  role = db.Column(db.String(20), nullable=False)
  animals = db.relationship('Animal', backref='owner', lazy=True, cascade="all, delete-orphan")
  orders = db.relationship('Order', backref='buyer', lazy=True, cascade="all, delete-orphan")

  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute.')

  @password.setter
  def password(self, password):
    self._password = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self._password, password)

  def __repr__(self):
    return f"<User id={self.id}, username={self.username}, role={self.role}>"

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self, username, role):
    self.username = username
    self.role = role
    db.session.commit()

class Animal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  breed = db.Column(db.String(50), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  orders = db.relationship('Order', backref='animal', lazy=True, cascade="all, delete-orphan")

  def __repr__(self):
    return f"<Animal id={self.id}, name={self.name}, breed={self.breed}, age={self.age}>"

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  status = db.Column(db.String(20), nullable=False, default='Pending')
  order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return f"<Order id={self.id}, status={self.status}, order_date={self.order_date}>"