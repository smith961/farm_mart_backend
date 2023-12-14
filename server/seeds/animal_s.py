from sqlalchemy import desc
from datetime import datetime
from config import db
from models.animal import Animal, TypeOfAnimal, BreedofAnimal,AnimalInventory
from models.user_info import User_Info, User

class TypeOfAnimalsSeeder:
  @staticmethod
  def get_animal_id_based_type(type_name):
    type_obj = TypeOfAnimal.query.filter_by(type_name=type_name).first()
    return type_obj.type_id if type_obj else None

  @staticmethod
  def get_all_types():
    types = TypeOfAnimal.query.all()
    return [type_obj.as_dict() for type_obj in types]

  @staticmethod
  def get_types_for_headers():
    types = TypeOfAnimal.query.all()
    types_data = []
    for type_obj in types:
      data_dict = {'typeName': type_obj.type_name, 'breedOfAnimals': []}
      breedofanimals = BreedofAnimal.query.filter_by(type_id=type_obj.type_id).all()
      for breed in breedofanimals:
        data_dict['breedOfAnimals'].append(breed.breed_name)
      types_data.append(data_dict)
    return types_data


class BreedOfAnimalsSeeder:
  @staticmethod
  def get_breed_id_based_breed(breed_name):
    breed = BreedofAnimal.query.filter_by(breed_name=breed_name).first()
    return breed.breed_id if breed else None

  @staticmethod
  def get_breeds_based_type_of_animal(type_id):
    breeds = BreedofAnimal.query.filter_by(type_id=type_id).all()
    return [breed.as_dict() for breed in breeds]


class AnimalsSeeder:
  @staticmethod
  def get_all_animals_based_on_type_of_animal(type_id):
    animals = db.session.query(Animal, BreedofAnimal).join(
      BreedofAnimal, Animal.breed_id == BreedofAnimal.breed_id
    ).filter(Animal.type_id == type_id).all()

    data_list = []
    for animal, breed in animals:
      data_dict = animal.as_dict()
      data_dict.update(breed.as_dict())
      data_list.append(data_dict)
    return data_list

  @staticmethod
  def get_all_animals_based_on_breed_of_animal(breed_id):
    animals = Animal.query.filter_by(breed_id=breed_id).all()
    return [animal.as_dict() for animal in animals]

  @staticmethod
  def get_single_animal(animal_id):
    animal = db.session.query(Animal, TypeOfAnimal, BreedofAnimal, AnimalInventory).join(
        TypeOfAnimal, Animal.type_id == TypeOfAnimal.type_id
    ).join(BreedofAnimal, Animal.breed_id == BreedofAnimal.breed_id).join(
        AnimalInventory, Animal.inventory_id == AnimalInventory.inventory_id
    ).filter(Animal.animal_id == animal_id).first()

    return animal.as_dict() if animal else None