from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os, json
import stripe
from apps.stripe_elements_single.hidden_account import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, \
                           STRIPE_WEBHOOK_SECRET

# IMPORTANT - INITIATE stripe WITH SECRET KEY
stripe.api_key = STRIPE_SECRET_KEY

''' -----------------------------------------------------
                PUBLIC FACING VIEWS
----------------------------------------------------- '''
class ElementsSubView(View):

    def get(self, request, **kwargs):

        # Set to None for now.
        context = None

        return render(request, 'stripe_elements_subscription/es_email.html', context=context)
