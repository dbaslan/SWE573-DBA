from django.contrib import admin
from .models import Post, Profile
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

admin.site.register(Post)
admin.site.register(Profile)

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }