from datetime import datetime
from config import db
from models.cart import OrderDetail, OrderItem, Cart
from models.animal import Animal, BreedofAnimal


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