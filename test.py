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

    def test_invalid_format_limit_posts(self):
        response = self.client.get('/posts?limit=asd')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid limit value', response.data.decode())

    def test_empty_data_response_photos(self):
        response = self.client.get('/photos?limit=0')
        self.assertEqual(response.status_code, 200)
        self.assertIn('No photos available', response.data.decode())  # Assume handling for empty data

    def test_404_route(self):
        response = self.client.get('/asd')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', response.data.decode())  # Custom 404 message

class TestContract(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('app.routes.get')
    def test_fetch_post(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'title': 'Test Post'}]
        response = self.app.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    @patch('main.requests.post')
    def test_set_limit(self, mock_post):
            mock_post.return_value.status_code = 200
            response = self.app.post('/set_display_limit', json={'limit': 10})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Display limit set to 10', response.data)

    @patch('app.routes.get')
    def test_fetch_photos(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'title': 'Test Photo'}]
        response = self.app.get('/photos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Photo', response.data)

    @patch('app.routes.get')
    def test_fetch_albums(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'title': 'Test Album 1'}, {'title': 'Test Album 2'}]
        response = self.app.get('/albums')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Album 1', response.data)
        self.assertIn(b'Test Album 2', response.data)

if __name__ == '__main__':
    unittest.main()
