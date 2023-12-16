from datetime import datetime
from config import bcrypt
from config import db
from models.auth import User

class Users():
    def add_user(self, user_object):
        db.session.add(user_object)
        db.session.commit()
    
    def get_single_user(self, user_email):
        user_object = User.query.filter_by(email = user_email).first()
        return user_object
    
    def update_password_with_user(self, user_id, user_new_password):
        updation = User.query.filter_by(id = user_id).update({
            User._password: bcrypt.generate_password_hash(user_new_password),
            User.updated_at: datetime.datetime.utcnow()
        })
        db.session.commit()
        return False if updation == 0 else True
