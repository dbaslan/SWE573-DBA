from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=32)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=30000)
    posted_date = models.DateTimeField(default=timezone.now)
    #memory_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
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
    content = models.TextField(max_length=3000)
    posted_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()