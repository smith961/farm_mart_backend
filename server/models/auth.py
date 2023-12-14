import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from server.config import db, app, bcrypt

class User(db.Model, SerializerMixin):
  __tablename__ = 'users'

  user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement= True)
  user_email = db.Column('user_email', db.String(250), nullable = False, unique = True)
  _user_password = db.Column('_user_password', db.String(250))
  created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = db.Column('updated_at', db.DateTime, default=datetime.utcnow, nullable=False)


  @hybrid_property
  def user_password(self):
    raise AttributeError('Password hashes may not be viewed.')

  @user_password.setter
  def user_password(self, password):
    user_password = bcrypt.generate_password_hash(
        password.encode('utf-8'))
    self._user_password = user_password.decode('utf-8')

  def authenticate(self, password):
    return bcrypt.check_password_hash(
      self._user_password, password.encode('utf-8'))

  def as_dict(self):
    return {
      'userId': self.user_id,
      'userEmail': self.user_email
    }


  with app.app_context():
    db.create_all()