import datetime
import base64
from server.config import db, app
from models.user import User



class User_Info(db.Model):
    __tablename__ = 'users_info'

    user_info_id = db.Column('user_id', db.Integer, primary_key = True, autoincrement = True)
    user_first_name = db.Column('user_first_name', db.String(255), nullable= False)
    user_last_name = db.Column('user_last_name', db.String(255), nullable= False)
    user_email = db.Column('email', db.String(255), nullable= False)
    user_phone_number =  db.Column('user_phone_number', db.String(255), nullable= False)
    user_id = db.Column('user_id', db.ForeignKey(
       User.user_id, ondelete='CASCADE', onupdate='CASCADE'), nullable= False, unique=True)
    created_at = db.Column('created_at', db.Datetime, default = datetime.datetime.utcnow, nullable = False )
    updated_at = db.Column('updated_at', db.Datetime, default = datetime.datetime.utcnow, nullable = False )


    def as_dict(self):
       return {
          'firstName': self.user_first_name,
          'lastName': self.user_last_name,
          'phoneNumber': self.user_phone_number,
          
       }



    with app.app_context():
     db.create_all()


