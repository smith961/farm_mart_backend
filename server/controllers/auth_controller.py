from flask import request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_restful import Resource
from config import app, api
from server.seeds.auth_s import Users
from server.models.auth import User

class Signup(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
    
        if not email or not password:
         return make_response({"msg": "Invalid data"}, 400)
        else:
            user_s = Users()
            user = User()
            user.email = email
            user._password = generate_password_hash(password)

        try:
            existing_user = user_s.get_single_user(email)
            user_s.add_user(user)
            return  make_response({"msg": "Successfully added"}, 201)
        except Exception as e:
            return make_response({"msg": "Email already exists"}, 400)
        

class Login(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return make_response({"msg": "Invalid data"}, 400)
    
        else:
            user_s = Users()

        existing_user = user_s.get_single_user(email)
        if not existing_user == None:
            isPasswordTrue = check_password_hash(
                existing_user._password, password)
            if isPasswordTrue:
                access_token = create_access_token(
                    identity={"email": email, "userId": existing_user.id}
                )
                refresh_token = create_refresh_token(
                    identity={"email": email, "userId": existing_user.id}
                )

                return make_response({"accessToken": access_token, "refreshToken": refresh_token, "user": {"email": existing_user.email,"user_id": existing_user.id}}, 201)
            else:
                 return make_response({"msg": "User doesn't exists"}, 400)
            

class AcessToken(Resource):
    @jwt_required(refresh = True)
    def get_access_token():
        user_s = Users()
        identity = get_jwt_identity()
        user = user_s.get_single_user(identity.get('user_email'))
        if user:
            access_token = create_access_token(identity=identity)
            return make_response({"accessToken": access_token, "user": identity}, 201)
        return make_response({"msg": "User doesn't exists"}, 401)


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(AcessToken, '/get-access-token', endpoint='get-access-token')
