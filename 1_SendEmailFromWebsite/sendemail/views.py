from django.shortcuts import render
from django.views import View
from sendemail.forms import SendEmailForm
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.core.mail import send_mail

EMAIL_FROM_ADDRESS = 'mark.john.wilson@gmail.com'

class FrontEndView(View):

    def __processForm(self, request, form, context):

        # Form is valid, get the data from the form
        send_email = form.cleaned_data['form_email']

        # Generate the new email message
        strNewSubject = "CONTACT FROM sendemail DJANGO APP"
        strNewMessage = f"Hello from a random user of sendemail Django App."

        # Use Django to send the email
        send_mail(
            strNewSubject,
            strNewMessage,
            EMAIL_FROM_ADDRESS,
            [send_email]
        )

        # Email sent and no error's
        return True

    def get(self, request, **kwargs):

        # Form initially called by get, so setup default context then
        # render the form
        form = SendEmailForm()
        context = {
                'form': form,
                'email_error': False,
                'email_error_description': '',
        }
        return render(request, 'index.html', context=context)

    def post(self, request, **kwargs):

        # Generate and validate the form
        form = SendEmailForm(request.POST)

        # Build a default context using the form and recaptcha keys.   Allow
        # room for an extra error
        context = {
                'form': form,
                'email_error': False,
                'email_error_description': '',
        }

        if form.is_valid():

            try:

                self.__processForm(request, form, context)
                return render(request, 'success.html', context=None)

            except Exception as Ex:

                context['email_error'] = True
                context['email_error_description'] = Ex.args[0]

            # Form was invalid, so just post it without changing context
            return render(request, 'index.html', context=context)

        else:
            # Form was invalid, so just post it without changing context
            return render(request, 'index.html', context=context)
