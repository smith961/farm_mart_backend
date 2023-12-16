import datetime
import base64
from server.config import db, app
from server.models.auth import User



class User_Info(db.Model):
    __tablename__ = 'users_info'

    id = db.Column('user_id', db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column('first_name', db.String(255), nullable= False)
    last_name = db.Column('last_name', db.String(255), nullable= False)
    email = db.Column('email', db.String(255), nullable= False)
    phone_number =  db.Column('phone_number', db.String(255), nullable= False)
    user_id = db.Column('user_id', db.ForeignKey(
       User.id, ondelete='CASCADE', onupdate='CASCADE'), nullable= False, unique=True)
    created_at = db.Column('created_at', db.Datetime, default = datetime.datetime.utcnow, nullable = False )
    updated_at = db.Column('updated_at', db.Datetime, default = datetime.datetime.utcnow, nullable = False )


    def as_dict(self):
       return {
          'firstName': self.first_name,
          'lastName': self.last_name,
          'phoneNumber': self.phone_number,
          
       }



    with app.app_context():
     db.create_all()


