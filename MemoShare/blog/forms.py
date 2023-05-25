from django import forms
from .models import Post, Profile


class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "tags", "location", "memory_date")
        widgets = {
            'memory_date': DateInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "Last_name", "birthdate", "location", "bio"]