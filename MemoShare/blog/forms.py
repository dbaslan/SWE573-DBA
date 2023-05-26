from django import forms
from .models import Post, Profile, User, Comment

class DateInput(forms.DateInput):
    input_type = 'date'

class EmailInput(forms.EmailInput):
    input_type = 'email'

# Form for making new post and editing
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "tags", "location", "memory_date", "image")
        widgets = {
            'memory_date': DateInput(),
        }

# Form for editing profile settings
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "birthdate", "location", "bio", "avatar"]
        widgets = {
            'birthdate': DateInput(),
        }

# Form for changing email address
class MailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            'email': EmailInput(),
        }

# Form for editing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

# Form for sending message to admin
class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)
