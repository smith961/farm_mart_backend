from sqlalchemy import desc
from datetime import datetime
from config import db
from models.animal import Animal, TypeOfAnimal, BreedofAnimal,AnimalInventory
from models.user_info import User_Info, User

class TypeOfAnimals():
    def get_type_id_based_type(self, type_name):
        type = TypeOfAnimal.query.filter_by(type_name=type_name).first()
        return type.id
    
    def  get_all_types(self):
        types = TypeOfAnimal.query.all()
        return [types.as_dict() for type in types]
    
    def get_types_for_headers(self):
        types = db.session.query(TypeOfAnimals).all()
        types_data = []
        for type in types:
            data_dict = {}
            data_dict['typeName'] = type.name
            breedofanimals= BreedofAnimal.query.filter_by(type_id = type.id).all()
            breedofanimals_data = []
            for breed in breedofanimals:
                breedofanimals_data.append(breed.breed_name)
            data_dict['breedOfAnimals'] = breedofanimals_data
            types_data.append(data_dict)
        return types_data

    
class BreedOfAnimals():
    def get_breed_Id_based_breed(self, breed_name):
        breed = BreedofAnimal.query.filter_by(breed_name=breed_name).first()
        return breed.id
    
    def get_breed_based_type_of_animal(self, type_id):
        breeds = BreedOfAnimals.query.filter_by(type_id = type_id).all()
        return [breed.as_dict() for breed in breeds]

class Animals():
    def get_all_animals_based_on_types_of_animal(self, type_id):
        animals = db.session.query(Animal,BreedofAnimal).join(
            BreedofAnimal,Animal.breed_id == BreedofAnimal.id
        ).filter(Animal.type_id == type_id).all()
        data_list = []
        for animal in animals:
            data_dict = {}
            data_dict.update(animal[0].as_dict())
            data_dict.update(animal[1].as_dict())
            data_dict.update(animal[2].as_dict())
            data_list.append(data_dict)
        return data_list
    
    def get_all_animals_based_on_breed_of_animal(self, breed_id):
        animals = Animal.query.filter_by(breed_id=breed_id).all()
        data_list = []
        for animal in animals:
            data_dict = {}
            data_dict.update(animal.as_dict())
            data_list.append(data_dict)
        return data_list

    def get_single_animal(self, animal_id):
        animal = db.session.query(Animal, TypeOfAnimal, BreedofAnimal, AnimalInventory).join(
            TypeOfAnimal, Animal.breed_id == TypeOfAnimal.id
        ).join(BreedofAnimal, Animal.breed_id == BreedofAnimal.id).join(
            AnimalInventory, Animal.inventory_id == AnimalInventory.id
        ).filter(Animal.id == animal_id).first()

        data_dict = {}
        for livestock in animal:
            data_dict.update(livestock.as_dict())
        return data_dict    