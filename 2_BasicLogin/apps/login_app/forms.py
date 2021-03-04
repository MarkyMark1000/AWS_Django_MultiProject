from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation

# Extend default django form for user registration to 
# add 'email'

# forms.Form
class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        label=("Email"),
        widget=forms.EmailInput(attrs={'autocomplete': 'new-email'}),
        help_text=("Please enter email.")
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")
