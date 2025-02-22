from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

from django import forms

class UserForm(forms.Form):
    username = forms.CharField(
        label='Username', 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email1 = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )
