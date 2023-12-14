from datetime import datetime
from config import db
from models.cart import OrderDetail, OrderItem, Cart
from models.animal import Animal, BreedofAnimal


class Carts():
  @staticmethod
  def get_user_cart(user_id):
    cart_items = db.session.query(Cart, Animal, BreedofAnimal).join(
        Animal, Cart.animal_id == Animal.animal_id
    ).join(
        BreedofAnimal, Animal.breed_id == BreedofAnimal.breed_id
    ).filter(Cart.user_id == user_id).all()

    data = []
    for cart_item in cart_items:
      cart_object = {
        **cart_item[0].as_dict(),
        **cart_item[1].as_dict(),
        **cart_item[2].as_dict(),
        'isAddedInCart': True
      }
      data.append(cart_object)

    return data

  @staticmethod
  def post_animal_in_cart(animal_id, quantity, user_id):
    cart_obj = Cart(
      quantity=quantity,
      user_id=user_id,
      animal_id=animal_id
    )
    db.session.add(cart_obj)
    db.session.commit()

    cart_item = db.session.query(Cart, Animal, BreedofAnimal).join(
      Animal, Cart.animal_id == Animal.animal_id
    ).join(
      BreedofAnimal, Animal.breed_id == BreedofAnimal.breed_id
    ).filter(Cart.user_id == user_id, Cart.animal_id == animal_id).first()

    if cart_item:
      return {
        **cart_item[0].as_dict(),
        **cart_item[1].as_dict(),
        **cart_item[2].as_dict(),
        'isAddedInCart': True
      }
    return None