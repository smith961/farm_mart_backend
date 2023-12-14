import sqlalchemy
from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from server.config import app,api
from server.seeds.user_info_s import UserInfos
from server.seeds.auth_s import Users
from flask import Blueprint
from server.exts import api


class User_Profile(Resource):
  @jwt_required()
  def user_profile():
    user_id = get_jwt_identity().get('userId')
    user_info_s = UserInfos()

    if request.method == 'GET':
      try:
        profile_data = user_info_s.get_user_profile(user_id)

        if profile_data:
            return make_response(profile_data, 200)
        else:
            return make_response({"msg": "No record found"}, 400)
      except Exception as e:
          return make_response({"msg":"Something went wrong, try again"}, 400)
    elif request.method == 'PUT':
      try:
        first_name = request.json.get('firstName')
        last_name = request.json.get('lastName')
        phone_number = request.json.get('phoneNumber')
        email = request.json.get('email')

        user_info_s.add_user_profile(user_id, first_name, last_name, phone_number,email )
        return make_response({"msg": "Profile successfully added"}, 201)
      # except sqlalchemy.exc.IntegrityError as e:
      #     return make_response({"msg": "Your profile already added"}, 400)
      except Exception as e:
            return make_response({"msg": "Something went wrong, try again"}, 400)


class UpdatePassword(Resource):
  @jwt_required()
  def user_update_password():
    user_id = get_jwt_identity().get('userId')
    user_s =  Users()

    if request.method == 'PUT':
      user_new_password = request.json.get('newPassword')
      updation_status = user_s.update_password_with_user(user_id, user_new_password)

      if updation_status:
        return make_response({"msg": "Profile password successfully updated"}, 201)
      else:
        return make_response({"msg": "Error occured, Please try again"}, 400)


api.add_resource(User_Profile, '/profile', endpoint='/profile')
api.add_resource(UpdatePassword, '/update-password', endpoint='/update-password')