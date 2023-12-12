from flask import Flask
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import User
from exts import db



app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

api = Api(app, doc='/docs')

# Model (serializer)
user_model=api.model
{
  "User",
  {
    "id": fields.Integer(),
    "title": fields.String(),
    "description": fields.String()
  }
}

@api.route('/hello')
class HelloResource(Resource):
  def get(self):
    return {"message": "Hello World!"}
  

@app.shell_context_processor
def make_shell_context():
  return {
    "db": db,
    "User": User
  }
  
  
if __name__ == '__main__':
  app.run(debug=True)