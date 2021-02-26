from django.shortcuts import render
from django.views import View
from sendemail.forms import SendEmailForm
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import SuspiciousOperation, ValidationError


class FrontEndView(View):

    def __processForm(self, request, form, context):

        # Form is valid, get the data from the form
        sender_email = form.cleaned_data['form_email']

        # Generate the new email message
        strNewSubject = "CONTACT FROM sendemail DJANGO APP"
        strNewMessage = f"Hello from a random user of sendemail Django App."

        # Please note that your role needs access to SES
        # for this to work.

        # Create a new SES resource and specify a region.   SES is in
        # eu-west-1 NOT eu-west-2
        client = boto3.client('ses', region_name="eu-west-1")

        # Try to send the email.
        # Yahoo prevents you from sending via ses, so I am going to send
        # an email to my yahoo from my gmail account.   At some point in
        # the future, I need to adjust this once I have a proper domain,
        # but I don't have time to do that yet. Both email addresses have
        # been authorised in SES. I cannot send to external email addresses
        # unless it is adjusted by AWS and I am not prepared to do this
        # yet.   For this reason, I cannot currently respond to the sender.

        tmpDestination = {'ToAddresses':
                            ["mark_john_wilson@yahoo.co.uk", ], }
        tmpMessage = {
                'Body': {
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': strNewMessage,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': strNewSubject,
                },
            }
        # Provide the contents of the email.
        response = client.send_email(
            Destination=tmpDestination,
            Message=tmpMessage,
            Source="mark.john.wilson@gmail.com"
        )

        # Email sent and no error's
        return True

    def get(self, request, **kwargs):

        # Form initially called by get, so setup default context then
        # render the form
        form = SendEmailForm()
        context = {
                'form': form,
        }
        return render(request, 'index.html', context=context)

    def post(self, request, **kwargs):

        # Generate and validate the form
        form = SendEmailForm(request.POST)

        # Build a default context using the form and recaptcha keys.   Allow
        # room for an extra error
        context = {
                'form': form,
        }

        if form.is_valid():

            self.__processForm(request, form, context)
            return render(request, 'success.html', context=None)

        else:
            # Form was invalid, so just post it without changing context
            return render(request, 'contact.html', context=context)
