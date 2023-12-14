from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from server.config import app, api
from server.models.animal import Animal
from server.seeds.animal_s import Animals, TypeOfAnimals, BreedOfAnimals

class AnimalProduce(Resource):
    @jwt_required()
    def get_animals():
        animal_s = Animals()
        type = request.args.get('type')
        breed = request.args.get('breed')
        if type:
            animal_type = TypeOfAnimals()
            try:
                type_id = animal_type.get_animal_id_based_type(type)
                data = animal_s.get_all_animals_based_on_types_of_animal(type_id)
                if len(data) !=0:
                    return make_response({"products": data}, 200)
                else:
                    return make_response({"msg": "No animals found"}, 400)
            except AttributeError:
                return make_response({"msg": "No animals for given type"}, 400)
        elif breed:
            animal_breed = BreedOfAnimals()
            try:
                breed_id = animal_breed.get_breed_Id_based_breed(breed)
                data = animal_s.get_all_animals_based_on_breed_of_animal(breed_id)
                if len(data) != 0:
                    return make_response({"animals": data}, 200)
                else:
                    return make_response({"msg": "No animals found"}, 400)
            except AttributeError: 
                return make_response({"msg": "No animals found for given breed"}, 400)
            

class AnimalProducById(Resource):
    @jwt_required()
    def get_one_animal(id):
        animal_s = Animals()
        try:
            data = animal_s.get_single_animal(id)
            if not data:
                return make_response({"msg": "No animal found"}, 400)
            else:
                return make_response(data, 200)
        except TypeError:
            return make_response({"msg": "Invalid id"}, 400)
        

class AllTypesOfAnimal():
    @jwt_required()
    def get_all_types():
        animal_type = TypeOfAnimals()
        data = animal_type.get_all_types()
        if len(data) !=0:
            return make_response({"types": data}, 200)
        else:
            return make_response({"msg": "No types found"}, 400)

class AllBreedOfAnimal():
    @jwt_required()
    def get_breed_of_animal():
        animal_type = TypeOfAnimals()
        type = request.args.get('type')
        if not type:
            return make_response({"msg": "Query param not correct"}, 400)
        else:
            type_id = animal_type.get_type_id_based_type(type)
            data = animal_type.get_breed_based_type_of_animal(type_id)
            if len(data) !=0:
                return make_response({"types": data}, 200)
            else:
                return make_response({"msg": "No types found"}, 400)


api.add_resource(AnimalProduce, '/animals', endpoint='animals')
api.add_resource(AnimalProducById, '/animals/<int: id>', endpoint='/animals/<int: id>')
api.add_resource(AllTypesOfAnimal, '/animals/types', endpoint='animals/types')
api.add_resource(AnimalProduce, '/animals/breeds', endpoint='animals/breeds')