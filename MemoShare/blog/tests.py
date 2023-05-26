from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Comment, Post, Profile
from django.urls import reverse
from .forms import PostForm, ProfileForm


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
            text='Text',
            posted_date=timezone.now(),
            memory_date=timezone.now(),
            location='Test Location',
            image='images/test.png'
        )

    # Test post creation
    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.text, 'Text')
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
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a profile for the test user
        self.profile = Profile.objects.create(
            user=self.user,
            name='Test User',
            bio='Test Bio',
            location='Test Location',
            birthdate='2000-01-01',
            avatar='profile_pics/test.png'
        )

    # Test profile creation
    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, 'Test User')
        self.assertEqual(self.profile.bio, 'Test Bio')
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


# Test Comment() model
class CommentTest(TestCase):

    def setUp(self):

        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test post
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='Text',
            posted_date=timezone.now(),
            memory_date=timezone.now(),
            location='Test Location',
            image='images/test.png'
        )

        # Create test comment
        self.comment = Comment.objects.create(
            text='Text',
            posted_date=timezone.now(),
            author=self.user,
            post=self.post
        )

    # Test comment creation
    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'Text')
        self.assertIsNotNone(self.comment.posted_date)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)

    # Test __str__() method
    def test_comment_string_representation(self):
        expected_str = self.comment.text
        self.assertEqual(str(self.comment), expected_str)


# Test PostForm() form
class PostFormTest(TestCase):

    def test_valid_post_form(self):

        # Create dictionary with valid data
        form_data = {
            'title': 'Test Post',
            'text': 'Text',
            'tags': 'tag1, tag2',
            'location': 'Test Location',
            'memory_date': '2022-01-01',
            'image': None
        }

        # Create form instance with data
        form = PostForm(data=form_data)

        # Check if form is valid
        self.assertTrue(form.is_valid())

    # Create dictionary with invalid data
    def test_invalid_post_form(self):
        form_data = {
            'title': '',
            'text': 'Text',
            'tags': 'tag1, tag2',
            'location': 'Test Location',
            'memory_date': '2022-01-01',
            'image': None
        }

        # Create form instance with data
        form = PostForm(data=form_data)

        # Check if form is invalid
        self.assertFalse(form.is_valid())


# Test ProfileForm() form
class ProfileFormTests(TestCase):

    def test_valid_profile_form(self):

        # Create dictionary with data
        form_data = {
            'name': 'John Doe',
            'birthdate': '2000-01-01',
            'location': 'Test Location',
            'bio': 'Text',
            'avatar': None
        }

        # Create form instance with data
        form = ProfileForm(data=form_data)

        # Check if form is valid
        self.assertTrue(form.is_valid())

    # Create dictionary with invalid data
    def test_invalid_profile_form(self):
        form_data = {
            'name': '',
            'birthdate': '2000-01-01',
            'location': 'Test Location',
            'bio': 'Text',
            'avatar': None
        }

        # Create form instance with data
        form = ProfileForm(data=form_data)

        # Check if form is invalid
        self.assertFalse(form.is_valid())