from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from server.config import app, api
from server.seeds.cart_s import Carts
from server.models.cart import OrderDetail, OrderItem, Cart


class User_Cart(Resource):
    @jwt_required
    def get_cart_by_user():
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
            
api.add_resource(User_Cart,'/cart', endpoint='/cart')