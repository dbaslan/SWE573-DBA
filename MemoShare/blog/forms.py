from django import forms
from .models import Post


class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "text", "tags", "location", "memory_date")
        widgets = {
            'memory_date': DateInput(),
        }