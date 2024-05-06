import unittest
from flask_testing import TestCase
from app import app 

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

class TestRoutes(BaseTestCase):
    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_posts_route(self):
        response = self.client.get('/posts?limit=10')
        self.assertEqual(response.status_code, 200)

    def test_photos_route(self):
        response = self.client.get('/photos?limit=5')
        self.assertEqual(response.status_code, 200)

    def test_albums_route(self):
        response = self.client.get('/albums')
        self.assertEqual(response.status_code, 200)

    def test_invalid_limit_posts(self):
        response = self.client.get('/posts?limit=-10')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid limit value', response.data.decode())

    def test_invalid_limit_photos(self):
        response = self.client.get('/photos?limit=-5')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid limit value', response.data.decode())
    def test_invalid_limit_albums(self):
        response = self.client.get('/albums?limit=-3')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid limit value', response.data.decode())


if __name__ == '__main__':
    unittest.main()
