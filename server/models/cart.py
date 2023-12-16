from datetime import datetime
from server.config import app, db
from server.models.user_info import User_Info
from server.models.animal import Animal

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
    
    with app.app_context():
        db.create_all()