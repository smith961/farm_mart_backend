from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User

class Signup(Resource):
    def post(self):
        user_data = request.get_json()
        user_email = user_data.get('user_email')
        user_password = user_data.get('user_password')

        if user_email and user_password:
            try:
                new_user = User(**user_data)
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
                return new_user.to_dict(), 201
            except IntegrityError:
                db.session.rollback()
                return {'error': 'User with this email already exists'}, 422

        return {'error': '422 Unprocessable Entity'}, 422

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.get(session['user_id'])
            return user.to_dict(), 200
        return {'error': '401 Unauthorized'}, 401

class Login(Resource):
    def post(self):
        user_data = request.get_json()
        user_email = user_data.get('user_email')
        user_password = user_data.get('user_password')

        user = User.query.filter_by(user_email=user_email).first()
        if user and user.authenticate(user_password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'error': '401 Unauthorized'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id', None)
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
