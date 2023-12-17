import base64
from datetime import datetime 
from config import db, app, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from server.config import db, app




class TypeOfAnimal(db.Model):
    __tablename__ = 'type_of_animal'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column('type_name', db.String(255), nullable = False)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable = False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable = False)

    def as_dict(self):
        return {
            'typeId': self.id,
            'typeName': self.type_name

        }
    

class BreedofAnimal(db.Model):
    __tablename__ = 'breed_of_animal'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    breed_name = db.Column('breed_name', db.String(255), nullable = False)
    breed_description = db.Column('breed_description', db.Text, nullable=False)
    type_id = db.Column('type_id', db.ForeignKey(TypeOfAnimal.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable= False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable= False)

    def as_dict(self):
        return {
            'breedId': self.id,
            'breedName': self.breed_name,
            'breedDescription': self.breed_description

    }


class AnimalInventory(db.Model):
    __tablename__ = 'animal_inventory'
    
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    inventory_quantity = db.Column('inventory_quantity', db.Integer, nullable=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            'inventoryId': self.inventory_id,
            'inventoryQuantity': self.inventory_quantity
        }
    

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    name = db.Column('name', db.String(250), nullable=False)
    description = db.Column('description', db.Text, nullable=False)
    price = db.Column('price', db.Float, nullable=False)
    type_id = db.Column('type_id', db.ForeignKey(TypeOfAnimal.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    breed_id = db.Column('breed_id', db.ForeignKey(BreedofAnimal.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    inventory_id= db.Column('inventory_id', db.ForeignKey(AnimalInventory.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            'animalId': self.id,
            'animalName': self.name,
            'animalDescription': self.description,
            'animalPrice': self.price
        }
    
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement= True)
    email = db.Column('email', db.String(250), nullable = False, unique = True)
    _password = db.Column('_password', db.String(250))
    created_at = db.Column('created_at', db.DateTime, default= datetime.datetime.utcnow, nullable= False)
    updated_at = db.Column('updated_at', db.DateTime, default= datetime.datetime.utcnow, nullable= False)


    @hybrid_property
    def _password(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @_password.setter
    def _password(self, password):
        _password = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._user_password = _password.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password, password.encode('utf-8'))
    
    def as_dict(self):
        return {
            'userId': self.id,
            'userEmail': self.email
        }

class User_Info(db.Model):
    __tablename__ = 'users_info'

    id = db.Column('user_id', db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column('first_name', db.String(255), nullable= False)
    last_name = db.Column('last_name', db.String(255), nullable= False)
    email = db.Column('email', db.String(255), nullable= False)
    phone_number =  db.Column('phone_number', db.String(255), nullable= False)
    user_id = db.Column('user_id', db.ForeignKey(
       User.id, ondelete='CASCADE', onupdate='CASCADE'), nullable= False, unique=True)
    created_at = db.Column('created_at', db.Datetime, default = datetime.datetime.utcnow, nullable = False )
    updated_at = db.Column('updated_at', db.Datetime, default = datetime.datetime.utcnow, nullable = False )


    def as_dict(self):
       return {
          'firstName': self.first_name,
          'lastName': self.last_name,
          'phoneNumber': self.phone_number,
          
       }



    with app.app_context():
     db.create_all()

class OrderDetail(db.Model):
    __tablename__ = 'order_detail'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(User_Info.user_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    total = db.Column('total', db.Integer, nullable=False)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            'orderDetailId': self.id,
            'userId': self.user_id,
            'total': self.total
        }

class OrderItem(db.Model):
    __tablename__= 'order_item'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    order_detail_id = db.Column('order_detail_id', db.ForeignKey(OrderDetail.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    animal_id = db.Column('animal_id', db.ForeignKey(Animal.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    quantity = db.Column('quantity', db.Integer, nullable=False)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            'orderItemId': self.id,
            'animalId': self.animal_id,
            'quantity': self.quantity
        }
    
class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column('quantity', db.Integer, nullable=False)
    user_id = db.Column('user_id', db.ForeignKey(User_Info.user_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    animal_id = db.Column('animal_id', db.ForeignKey(Animal.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            'cartId': self.id,
            'quantity': self.quantity,
            'animalId': self.animal_id
        }
    
