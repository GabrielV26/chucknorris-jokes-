from django import forms
from .models import Joke

class JokeForm(forms.ModelForm):
    class Meta:
        model = Joke
        fields = ['text']
