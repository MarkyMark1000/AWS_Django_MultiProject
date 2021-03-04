from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SendEmailForm(UserCreationForm):

    username = forms.CharField(
        label=("Username"),
        strip=False,
        widget=forms.TextInput(attrs={'required': 'required',
                                      'minlength': '3',
                                      'maxlength': '30',
                                      'title': 'A Username between 3 and 30'
                                         ' characters is required.'
                                     }),
        help_text="Enter username",
    )
    email = forms.CharField(
        label=("Email"),
        strip=False,
        widget=forms.EmailInput(attrs={'required': 'required',
                                      'minlength': '3',
                                      'maxlength': '100',
                                      'title': 'An Email Address between 3 and 100'
                                         ' characters is required.'
                                     }),
        help_text="Enter email",
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("username", "email", 'password1', 'password2')
