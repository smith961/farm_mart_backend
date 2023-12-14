from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from server.config import app, api
from server.seeds.animal_s import TypeOfAnimals


class Home(Resource):
    def get_home_page():
        return make_response({"msg": "Welcome to Farmmart"}, 200)
    
class BreedsIndex(Resource):
    @jwt_required()
    def header_types_of_animals():
        types_of_animals = TypeOfAnimals()
        try:
            types = types_of_animals.get_types_for_headers()
            return make_response({"types": types }, 200)
        except Exception as e:
            return make_response({"msg": "Something went wrong, try again"}, 400)
           





api.add_resource(Home, '/', endpoint='/')
api.add_resource(BreedsIndex, '/breeds', endpoint='/breeds')