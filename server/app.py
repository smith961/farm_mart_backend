from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, User_Info, Admin, Farmer

class Signup(Resource):
    def post(self):
        user_first_name = request.get_json().get('user_first_name')
        user_last_name = request.get_json().get('user_last_name')
        user_email =  request.get_json().get(' user_email')
        user_password = request.get_json().get('user_password')
        user_phone_number = request.get_json().get('user_phone_number')
        

        if user_email and user_password :
            new_user = User(user_first_name=user_first_name,
                            user_last_name = user_last_name,
                            user_email = user_email,
                            user_phone_number = user_phone_number
                            )
            new_user.user_password = user_password

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            
            return new_user.to_dict(), 201

        return {'error': '422 Unprocessable Entity'}, 422
    

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200
        return {'error': '401 Resource not found'}, 401

class Login(Resource):
    def post(self):
        user_email = request.get_json()['user_email']
        user_password = request.get_json()['user_password']

        user = User.query.filter(User.user_email == user_email).first()
        if user and user.authenticate(user_password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'error': '401 Unauthorized'}, 401
    

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        else:
            return {'error': '401 Unauthorized'}, 401
    

class AnimalIndex(Resource):
    pass


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(AnimalIndex, '/animals', endpoint='animals')


if __name__ == '__main__':
    app.run(port=5555, debug=True)