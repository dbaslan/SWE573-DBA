from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Profile
from django.urls import reverse

# Test info page
class AboutTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "blog/about.html")

# Test home page
class HomeTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("post_list"))
        self.assertTemplateUsed(response, "blog/post_list.html")

# Test Post() model
class PostTests(TestCase):

    def setUp(self):

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create test post
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='This is the test post text.',
            posted_date=timezone.now(),
            memory_date=timezone.now(),
            location='Test Location',
            image='images/test.png'
        )

    # Test post creation
    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.text, 'This is the test post text.')
        self.assertIsNotNone(self.post.posted_date)
        self.assertIsNotNone(self.post.memory_date)
        self.assertEqual(self.post.location, 'Test Location')
        self.assertEqual(self.post.image, 'images/test.png')

    # Test __str__() method
    def test_post_string_representation(self):
        expected_str = self.post.title
        self.assertEqual(str(self.post), expected_str)

# Test Profile() model
class ProfileTest(TestCase):

    def setUp(self):

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a profile for the test user
        self.profile = Profile.objects.create(
            user=self.user,
            name='Test User',
            bio='This is the test user bio',
            location='Test Location',
            birthdate='2000-01-01',
            avatar='profile_pics/test.png'
        )

    # Test profile creation
    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, 'Test User')
        self.assertEqual(self.profile.bio, 'This is the test user bio')
        self.assertEqual(self.profile.location, 'Test Location')
        self.assertEqual(self.profile.birthdate, '2000-01-01')
        self.assertEqual(self.profile.avatar, 'profile_pics/test.png')

    # Test __str__() method 
    def test_profile_str(self):
        expected_str = self.user.username
        self.assertEqual(str(self.profile), expected_str)

    # Test automatic creation of profile on User creation
    def test_profile_auto_creation(self):
        new_user = User.objects.create_user(
            username='newuser',
            password='newpassword'
        )
        profile = Profile.objects.get(user=new_user)
        self.assertIsNotNone(profile)