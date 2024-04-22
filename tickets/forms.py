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
        fields = ['title', 'description', 'assigned_team', 'assigned_member', 'status']

    def __init__(self, *args, **kwargs):
        super_user = kwargs.pop('super_user', False)
        super().__init__(*args, **kwargs)

        if not super_user:
            self.fields['assigned_team'].disabled = True
            self.fields['assigned_member'].disabled = True


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
 
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
