from datetime import datetime
from config import db, app
from models import user_info

class TypeOfAnimal(db.Model):
  __tablename__ = 'type_of_animal'

  type_id = db.Column('type_id', db.Integer, primary_key=True, autoincrement=True)
  type_name = db.Column('type_name', db.String(255), nullable = False)
  created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)  
  updated_at = db.Column('updated_at', db.DateTime, default=datetime.utcnow, nullable=False)  


  def as_dict(self):
    return {
      'typeId': self.type_id,
      'typeName': self.type_name

    }


class BreedofAnimal(db.Model):
  __tablename__ = 'breed_of_animal'

  breed_id = db.Column('breed_id', db.Integer, primary_key=True, autoincrement=True)
  breed_name = db.Column('breed_name', db.String(255), nullable = False)
  breed_description = db.Column('breed_description', db.Text, nullable=False)
  type_id = db.Column('type_id', db.ForeignKey(TypeOfAnimal.type_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

  created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = db.Column('updated_at', db.DateTime, default=datetime.utcnow, nullable=False)

  def as_dict(self):
    return {
      'breedId': self.breed_id,
      'breedName': self.breed_name,
      'breedDescription': self.breed_description

  }


class AnimalInventory(db.Model):
  __tablename__ = 'animal_inventory'

  inventory_id = db.Column('inventory_id', db.Integer, primary_key=True, autoincrement=True)
  inventory_quantity = db.Column('inventory_quantity', db.Integer, nullable=True)
  created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False) 
  updated_at = db.Column('updated_at', db.DateTime, default=datetime.utcnow, nullable=False)  

  def as_dict(self):
    return {
      'inventoryId': self.inventory_id,
      'inventoryQuantity': self.inventory_quantity
    }


class Animal(db.Model):
  __tablename__ = 'animals'

  animal_id = db.Column('animal_id', db.Integer, primary_key=True, autoincrement = True)
  name = db.Column('name', db.String(250), nullable=False)
  description = db.Column('description', db.Text, nullable=False)
  price = db.Column('price', db.Float, nullable=False)
  type_id = db.Column('type_id', db.ForeignKey(TypeOfAnimal.type_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
  breed_id = db.Column('breed_id', db.ForeignKey(BreedofAnimal.breed_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
  inventory_id= db.Column('inventory_id', db.ForeignKey(AnimalInventory.inventory_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
  created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
  updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)

  def as_dict(self):
    return {
      'animalId': self.animal_id,
      'animalName': self.name,
      'animalDescription': self.description,
      'animalPrice': self.price
    }

  with app.app_context():
    db.create_all()