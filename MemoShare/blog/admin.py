from django.contrib import admin
from django import forms
from .models import Post, Profile
from easy_maps.widgets import AddressWithMapWidget

class PostAdmin(admin.ModelAdmin):
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'location': AddressWithMapWidget({'class': 'vTextField'})
            }

admin.site.register(Post)
admin.site.register(Profile)
