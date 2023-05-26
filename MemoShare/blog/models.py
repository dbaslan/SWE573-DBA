from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager
from django_google_maps import fields as map_fields


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=30000)
    posted_date = models.DateTimeField(default=timezone.now)
    memory_date = models.DateTimeField(blank=True, null=True)
    location = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(get_user_model(), related_name='liked_posts', through='Like')


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return '{} likes {}'.format(self.user.username, self.post.title)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])

class Comment(models.Model):
    text = models.TextField(max_length=3000)
    posted_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=155, null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    location = map_fields.AddressField(max_length=200, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    follows = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers")

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()