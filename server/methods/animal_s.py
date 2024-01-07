from sqlalchemy import desc
from datetime import datetime
from config import db, bcrypt
from models.animal import User_Info, User, Animal,TypeOfAnimal,BreedofAnimal,AnimalInventory,OrderDetail,OrderItem,Cart





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

class Users():
    def add_user(self, user_object):
        db.session.add(user_object)
        db.session.commit()
    
    def get_single_user(self, user_email):
        user_object = User.query.filter_by(email = user_email).first()
        return user_object
    
    def update_password_with_user(self, user_id, user_new_password):
        updation = User.query.filter_by(id = user_id).update({
            User._password: bcrypt.generate_password_hash(user_new_password),
            User.updated_at: datetime.datetime.utcnow()
        })
        db.session.commit()
        return False if updation == 0 else True

class Carts():

    def get_user_cart(self, user_id):
        cart = db.session.query(Cart, Animal, BreedofAnimal).join(
            Animal, Cart.animal_id == Animal.id
        ).join(
            BreedofAnimal, Animal.breed_id == BreedofAnimal.id
        ).filter(Cart.user_id == user_id).all()
        data = []
        for livestock in cart:
            cart_object = {}
            cart_object.update(livestock[0].as_dict())
            cart_object.update(livestock[1].as_dict())
            cart_object.update(livestock[2].as_dict())
            cart_object.update(livestock[3].as_dict())
            cart_object['isAddedInCart'] = True
            data.append(cart_object)
        return data
    
    def post_animal_in_cart(self, animal_id, quantity, user_id):
        cart_obj = Cart(
            quantity = quantity,
            user_id = user_id,
            animal_id = animal_id
        )
        db.session.add(cart_obj)
        cart = db.session.query(Cart, Animal, BreedofAnimal).join(
            Animal, Cart.animal_id == Animal.id
        ).join(
            BreedofAnimal, Animal.breed_id == BreedofAnimal.id
        ).filter(Cart.user_id == user_id, Cart.animal_id == animal_id).all()

        if len(cart) > 1:
            return None
        data = {}
        for livestock in cart[0]:
            data.update(livestock.as_dict())
            db.session.commit()
            return data
        
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