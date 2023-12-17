from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token,create_refresh_token
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlalchemy
from config import app, api
from models.animal import Animal,User, OrderDetail,OrderItem,Cart,User_Info
from methods.animal_s import Animals, TypeOfAnimals, BreedOfAnimals, Users,Carts, UserInfos





class AnimalProduce(Resource):
    @jwt_required()
    def get():
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
    def get(id):
        animal_s = Animals()
        try:
            data = animal_s.get_single_animal(id)
            if not data:
                return make_response({"msg": "No animal found"}, 400)
            else:
                return make_response(data, 200)
        except TypeError:
            return make_response({"msg": "Invalid id"}, 400)
        

class AllTypesOfAnimal(Resource):
    @jwt_required()
    def get():
        animal_type = TypeOfAnimals()
        data = animal_type.get_all_types()
        if len(data) !=0:
            return make_response({"types": data}, 200)
        else:
            return make_response({"msg": "No types found"}, 400)

class AllBreedOfAnimal():
    @jwt_required()
    def get():
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

class AcessToken(Resource):
    @jwt_required(refresh = True)
    def get(self):
        user_s = Users()
        identity = get_jwt_identity()
        user = user_s.get_single_user(identity.get('user_email'))
        if user:
            access_token = create_access_token(identity=identity)
            return make_response({"accessToken": access_token, "user": identity}, 201)
        return make_response({"msg": "User doesn't exists"}, 401)       

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
            
class User_Cart(Resource):
    @jwt_required()
    def get():
        user_id = get_jwt_identity().get('userId')
        cart_s = Carts()

        if request.method == 'GET':
            try:
                cart = Carts.get_user_cart(user_id)
                if len(cart) == 0:
                    return make_response({'msg': 'No cart found'}, 400)
                return make_response({'cart': cart}, 200)
            except Exception as e:
                return make_response({"msg": "Something went wrong"}, 400)
            

        if request.method == 'POST':
            try:
               animal_id = request.json.get('animalId')
               quantity = request.json.get('quantitiy')

               res = cart_s.post_animal_in_cart(animal_id, quantity, user_id)
               if not res:
                   return make_response({"msg": "Product already added"}, 400)
               return make_response({'cart': res, 'msg': 'Product added in cart'}, 201)
            except Exception as e:
               print(e)
               return make_response({'msg':'Something went wrong'}, 400)

class Home(Resource):
    def get(self):
        return make_response({"msg": "Welcome to Farmmart"}, 200)
    
class BreedsIndex(Resource):
    @jwt_required()
    def get():
        types_of_animals = TypeOfAnimals()
        try:
            types = types_of_animals.get_types_for_headers()
            return make_response({"types": types }, 200)
        except Exception as e:
            return make_response({"msg": "Something went wrong, try again"}, 400)

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
            except sqlalchemy.exc.IntegrityError as e:
                return make_response({"msg": "Your profile already added"}, 400)
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
api.add_resource(Home, '/', endpoint='/')
api.add_resource(BreedsIndex, '/breeds', endpoint='/breeds')          
api.add_resource(User_Cart,'/cart', endpoint='/cart')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(AcessToken, '/get-access-token', endpoint='get-access-token')
api.add_resource(AnimalProduce, '/animals', endpoint='animals')
api.add_resource(AnimalProducById, '/animals/<int:id>', endpoint='/animals/<int: id>')
api.add_resource(AllTypesOfAnimal, '/animals/types', endpoint='animals/types')
api.add_resource(AnimalProduce, '/animals/breeds', endpoint='animals/breeds')