from django import forms
from .models import maintickets
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import maintickets

class TicketForm(forms.ModelForm):
    class Meta:
        model = maintickets
        fields = ['title', 'description', 'status']   # Include necessary fields
        exclude = ['user']  # Exclude fields not to be filled out by the form
    file = forms.FileField(required=False)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
 