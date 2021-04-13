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

class ElementsPricesView(View):

    def get(self, request, **kwargs):

        # Set to None for now.
        context = None

        return render(request, 'stripe_elements_subscription/es_prices.html', context=context)

class ElementsSubPriceView(View):

    def get(self, request, **kwargs):

        # Get the session_id passed in from create_checkout_session
        price = request.GET.get('price', '')

        context = {
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
            'price': price
        }

        return render(request, 'stripe_elements_subscription/es_subscribe.html', context=context)

class ElementsSubAccountView(View):

    def get(self, request, **kwargs):

        context = {
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
        }

        return render(request, 'stripe_elements_subscription/es_account.html', context=context)

class ElementsCancelView(View):

    def get(self, request, **kwargs):

        # Get the session_id passed in from create_checkout_session
        subscription_id = request.GET.get('subscription_id', '')

        context = {
            'STRIPE_SUBSCRIPTION_ID': subscription_id,
        }

        return render(request, 'stripe_elements_subscription/es_cancel.html', context=context)

''' -----------------------------------------------------
            INTERFACES FOR JAVASCRIPT - FRONT END
----------------------------------------------------- '''
@csrf_exempt
def create_customer_view(request):

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    data = json.loads(str(request.body, encoding='utf-8'))

    try:
        # Create a new customer object
        customer = stripe.Customer.create(email=data['email'])

        # We are going to store the customer id in a cookie.   If you had an account
        # based system, you could save it in the database.
        response = JsonResponse({'customer':customer.id})
        response.set_cookie('customer', customer.id)

        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@csrf_exempt
def create_subscription_view(request):

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    data = json.loads(str(request.body, encoding='utf-8'))

    # Simulating authenticated user. Lookup the logged in user in your
    # database, and set customer_id to the Stripe Customer ID of that user.
    customer_id = request.COOKIES.get('customer')

    try:
        payment_method = stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=customer_id,
        )

        # priceLookupKey should contain something like Basic or Premium, so
        # we convert this into an actual stripe price here from the stripe dashoard
        if data['priceLookupKey'].upper() == "BASIC":
            price_id = "price_1IXkXPLnm61uJv5f8369c8Wl"
        elif data['priceLookupKey'].upper() == "PREMIUM":
            price_id = "price_1IXkYoLnm61uJv5fvwF7oxzM"

        # Create the subscription
        # (priceLookupKey comes from subscribe, the 'get' 'price' parameter)
        subscription = stripe.Subscription.create(
            default_payment_method=payment_method.id,
            customer=customer_id,
            items=[{
                'price': price_id
            }],
            expand=['latest_invoice.payment_intent'],
        )
        return JsonResponse({'subscription':subscription})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def list_subscriptions_view(request):

    # Designed for post requests.
    if request.method != 'GET':
        return HttpResponse(status=404)

    # Simulating authenticated user. Lookup the logged in user in your
    # database, and set customer_id to the Stripe Customer ID of that user.
    customer_id = request.COOKIES.get('customer')

    try:
         # Cancel the subscription by deleting it
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            status='all',
            expand=['data.default_payment_method']
        )
        return JsonResponse({'subscriptions':subscriptions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@csrf_exempt
def cancel_subscription_view(request):

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    data = json.loads(str(request.body, encoding='utf-8'))

    try:
         # Cancel the subscription by deleting it
        deletedSubscription = stripe.Subscription.delete(data['subscriptionId'])
        return JsonResponse({'subscription':deletedSubscription})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

''' -----------------------------------------------------
                    WEB HOOK CODE
----------------------------------------------------- '''
@csrf_exempt
def my_webhook_view(request):

    '''
    To test, run this is another shell:
    stripe listen --forward-to localhost:8080/stripe_sub_webhook/
    '''

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    request_data = json.loads(str(request.body, encoding='utf-8'))

    # Unsure about why this is here - taken from original tutorial.
    if STRIPE_WEBHOOK_SECRET:

        # Retrieve the event by verifying the signature using the raw
        # body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')

        try:
            event = stripe.Webhook.construct_event(payload=request.body,
                                                sig_header=signature,
                                                secret=STRIPE_WEBHOOK_SECRET)
            data = event['data']
        except Exception as e:
            return JsonResponse({'error': e.args[0]}, status=500)
        
        # Get the type of webhook event sent - used to
        # check the status of PaymentIntents.
        event_type = event['type']

    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        print('\n')
        print('*'*20)
        print("invoice.paid")
        print("You probably need to update the database to provision the data.")
        print('*'*20)
    
    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print('\n')
        print('*'*20)
        print("invoice.payment_failed")
        print("You probably need to update the database.")
        print('*'*20)
    
    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print('\n')
        print('*'*20)
        print("customer.subscription.deleted")
        print("You probably need to update the database.")
        print('*'*20)

    return JsonResponse({'status': 'success'})
