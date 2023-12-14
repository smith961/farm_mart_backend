from datetime import datetime
from config import bcrypt, db
from models.auth import User

class Users():
  @staticmethod
  def add_user(self, user_object):
    db.session.add(user_object)
    db.session.commit()

  @staticmethod
  def get_single_user(self, user_email):
    user_object = User.query.filter_by(user_email = user_email).first()
    return user_object

  @staticmethod
  def update_password_with_user(self, user_id, user_new_password):
    user = User.query.get(user_id)
    if user:
      user._user_password = bcrypt.generate_password_hash(user_new_password).decode('utf-8')
      user.updated_at = datetime.utcnow()
      db.session.commit()
      return True
    return False