import unittest
from main import create_app
from config import TestConfig
from exts import db
from datetime import datetime

class APITestCase(unittest.TestCase):

  def setUp(self):
    self.app = create_app(TestConfig)
    self.client = self.app.test_client()

    with self.app.app_context():
      db.create_all()

  def test_signup(self):
      response = self.client.post('/signup', json={
        'user_email': 'estheradeiye@gmail.com',
        'user_password': 'password'
      })

      status_code = response.status_code
      self.assertEqual(status_code, 201)

  def test_login(self):
      self.client.post('/signup', json={
        'user_email': 'estheradeiye@gmail.com',
        'user_password': 'password'
      })

      response = self.client.post('/login', json={
          'user_email': 'estheradeiye@gmail.com',
          'user_password': 'password'
      })

      status_code = response.status_code
      self.assertEqual(status_code, 200)

  def test_get_animals(self):
      response = self.client.get('/animals')

      status_code = response.status_code
      self.assertEqual(status_code, 200)

  def test_add_to_cart(self):
    login_response = self.client.post('/login', json={
        'user_email': 'testuser@example.com',
        'user_password': 'password'
    })

    access_token = login_response.json['access_token']

      # Now, add an animal to the cart
    response = self.client.post('/add_to_cart', json={
        'animal_id': 1,
        'quantity': 2
    }, headers={'Authorization': f'Bearer {access_token}'})

    status_code = response.status_code
    self.assertEqual(status_code, 201)

  # I need to add more test methods

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
    unittest.main()
