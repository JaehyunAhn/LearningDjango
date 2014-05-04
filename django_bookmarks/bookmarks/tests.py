from django.test import TestCase
from django.test.client import Client

# Create your tests here.
class ViewTest(TestCase):
    fixtures = ['test_data.json'] # p.252 Test database storage
    def setUp(self):
        self.client = Client()

    def test_register_page(self):
        data = {
            'username'  : 'test_user',
            'email'     : 'test_user@example.com',
            'password1' : 'pass123',
            'password2' : 'pass123',
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, 302)

    def test_bookmark_save(self):
        response = self.client.login (
            '/save/', 'test', 'test'
        )
        self.assertTrue(response) # Error occurred (p.251)
        # To solve this problem, we have to use "fixtures" function

        data = {
            'url'   : 'http://www.microsoft.com',
            'title' : 'Microsoft',
            'tags'  : 'test-tag'
        }
        response = self.client.post('/save/', data)
        self.assertEqual(response.status_code, 302) # Move page 302 cmd

        response = self.client.get('/user/test')
        self.assertTrue('http://www.microsoft.com' in response.content)
        self.assertTrue('Microsoft' in response.content)
        self.assertTrue('test-tag' in response.content)