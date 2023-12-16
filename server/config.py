import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager

DATABASE_URI = 'postgresql://smith:xQUCDiASx0OUaUy2yyV9of7bnWfuZOFS@dpg-clv06q5a73kc73blh9t0-a.oregon-postgres.render.com/farmmart'
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)

jwt = JWTManager(app)
