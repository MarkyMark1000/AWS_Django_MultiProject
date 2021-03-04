from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views import View
from apps.login_app.forms import CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
# from django.db import IntegrityError

# The following tutorials may be useful:
# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m


class CustomUserCreationView(View):

    def get(self, request, **kwargs):

        # Form initially called by get, so setup default context then
        # render the form
        form = CustomUserCreationForm()
        context = {'form': form,}
        return render(request, 'register.html', context=context)

    def post(self, request, **kwargs):

        # Form called by post, so populate form, process it and
        # display appropriate template.
        form = CustomUserCreationForm(request.POST)
        context = {'form': form,}

        if form.is_valid():
            # Initial Save
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
        else:
            # Display the form again
            return render(request, 'register.html', context=context)

class ActivationSentView(View):

    def get(self, request, **kwargs):

        return render(request, 'activation_sent.html')

class ActivateView(View):

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # checking if the user exists, if the token is valid.
        if user is not None and account_activation_token.check_token(user, token):
            # if valid set active true 
            user.is_active = True
            # set signup_confirmation true
            user.profile.signup_confirmation = True
            user.save()
            login(request, user)
            return redirect('frontend')
        else:
            return render(request, 'activation_invalid.html')