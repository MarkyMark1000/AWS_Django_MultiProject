from django.shortcuts import render
from django.views import View
from parallax.forms import ParallaxForm
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.core.mail import send_mail

class Page1View(View):

    def get(self, request, **kwargs):

        return render(request, 'page1.html', context=None)

class Page2View(View):

    def get(self, request, **kwargs):

        return render(request, 'page2.html', context=None)

class Page3View(View):

    def get(self, request, **kwargs):

        return render(request, 'page3.html', context=None)
