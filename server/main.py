from flask import Flask
from flask_restx import Api, Resource, fields
from server.config import DevConfig
from models import User
from exts import db



app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

api = Api(app, doc='/docs')
  
  
if __name__ == '__main__':
  app.run(debug=True)