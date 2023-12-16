from config import db
from models.user_info import User_Info
from models.animal import Animal,BreedofAnimal
from datetime import datetime

class UserInfos():
    def get_user_profile(self, user_id):
        user_info = User_Info.query.filter_by(user_id=user_id).first()
        if not user_info:
            return None
        return user_info.as_dict()
    
    def add_user_profile(self, user_id, first_name, last_name,
                         phone_number,email):
        updation = User_Info.query.filter_by(user_id=user_id).update({
            User_Info.first_name:first_name,
            User_Info.last_name:last_name,
            User_Info.phone_number:phone_number,
            User_Info.email:email,
            User_Info.user_id:user_id,
            User_Info.updated_at: datetime.datetime.utcnow()
         })
        if updation == 0:
            user_info = User_Info(
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number,
                email = email,
                user_id = user_id,
                created_at = datetime.datetime.utcnow(),
                updated_at = datetime.datetime.utcnow()
            )
            db.session.add(user_info)
            db.session.commit()