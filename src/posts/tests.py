from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .models import Post

class PostsTestCase(TestCase):

    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_loggedin_index(self):
        client = Client()
        self.test_user = get_user_model().objects.create_user(
            nickname='testuser',
            email='test@example.com',
            password='password1')
        client.login(email='test@example.com',password='password1')
        response = client.get('/')
        # self.assertEqual(response.status_code, 200)

        client.post('/create/', {'text': '本文', 'photo': ''})
        latest_post = Post.objects.latest('created_at')
        self.assertEqual(latest_post.text, '本文')
