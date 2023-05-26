from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, User

class UnitTest(TestCase):
    def setUp(self):

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create test posts
        self.post1 = Post.objects.create(
            title='Test Post',
            text='This is a test.',
            author=self.user
        )
        self.post2 = Post.objects.create(
            title='Another Test Post 2',
            text='This is another test.',
            author=self.user
        )
        self.post3 = Post.objects.create(
            title='Yet Another Test Post',
            text='This is yet another test.',
            author=self.user
        )

 	# Test post_list()
    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)
        self.assertContains(response, self.post3.title)

    # Test post_detail()
    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    # Test post_new()
    def test_create_post_view(self):
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_post'), {'title': 'New Post', 'text': 'Hello World.'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 3)