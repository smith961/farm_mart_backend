import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from server.config import db, app, bcrypt

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
    

    with app.app_context():
        db.create_all()