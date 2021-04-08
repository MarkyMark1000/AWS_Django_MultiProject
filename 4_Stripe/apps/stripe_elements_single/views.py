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
class CheckoutView(View):

    def get(self, request, **kwargs):

        intent = stripe.PaymentIntent.create(
            amount=1499,
            currency='gbp',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )

        context = {
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
            'CLIENT_SECRET': intent.client_secret
        }

        return render(request, 'stripe_elements_single/checkout.html', context=context)

class Checkout2View(View):

    def get(self, request, **kwargs):

        intent = stripe.PaymentIntent.create(
            amount=1499,
            currency='gbp',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )

        context = {
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
            'CLIENT_SECRET': intent.client_secret
        }

        return render(request, 'stripe_elements_single/checkout_2.html', context=context)

''' -----------------------------------------------------
                Interface Code for Javascript
----------------------------------------------------- '''
@csrf_exempt
def create_payment_intent_view(request):

    """
    Create a payment intent that can be used by the javascript in the client

    This section of code could be changed so that purchases are posted via
    the body and then the payment intent, ie price and currency is calculated
    using database data rather than client data.
    """

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    # Could be used to calculate prices of a shopping list etc.
    data = json.loads(str(request.body, encoding='utf-8'))

    try:
        # Create a PaymentIntent with the order amount and currency
        # (hard-coded for now)
        intent = stripe.PaymentIntent.create(
            amount=1499,
            currency='GBP'
        )

        # Send publishable key and PaymentIntent details to client
        return JsonResponse({'publishableKey': STRIPE_PUBLIC_KEY, 'clientSecret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

''' -----------------------------------------------------
                    WEB HOOK CODE
----------------------------------------------------- '''
@csrf_exempt
def my_webhook_view(request):

    '''
    To test, run this is another shell:
    stripe listen --forward-to localhost:8080/stripe_elements_webhook/
    '''

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    request_data = json.loads(str(request.body, encoding='utf-8'))

    if STRIPE_WEBHOOK_SECRET:

        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        
        try:
            event = stripe.Webhook.construct_event(payload=request.body,
                                                   sig_header=signature,
                                                   secret=STRIPE_WEBHOOK_SECRET)
            data = event['data']
        except Exception as e:
            return JsonResponse({'error': e.args[0]}, status=500)

        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']

    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('*'*20)
        print('WEBHOOK:')
        print('*'*20)
        print('💰 Payment received!')
        print('*'*20)
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('*'*20)
        print('WEBHOOK:')
        print('*'*20)
        print('❌ Payment failed.')
        print('*'*20)

    return JsonResponse({'status': 'success'})
