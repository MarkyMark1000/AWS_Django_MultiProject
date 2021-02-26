from django import forms


class SendEmailForm(forms.Form):
    form_email = forms.CharField(widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Email *',
                                'required': 'required',
                                'minlength': '3',
                                'maxlength': '100',
                                'title': 'An Email Address between 3 and 100'
                                         ' characters is required.'
                                }),)
