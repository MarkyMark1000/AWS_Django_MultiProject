from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os, json
import stripe
from apps.stripe_checkout_subscription.hidden_account import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, \
                           STRIPE_WEBHOOK_SECRET

# IMPORTANT - INITIATE stripe WITH SECRET KEY
stripe.api_key = STRIPE_SECRET_KEY

''' -----------------------------------------------------
                PUBLIC FACING VIEWS
----------------------------------------------------- '''

class BasicSubscriptionView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_subscription/basic.html', context=None)

class SubCancelView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_subscription/cancel.html', context=None)

class SubSuccessView(View):

    def get(self, request, **kwargs):

        # Get the session_id passed in from create_checkout_session
        session_id = request.GET.get('session_id', '')

        context = {
            'session_id': session_id
        }

        return render(request, 'stripe_checkout_subscription/success.html', context=context)

class SubFinishedBillingView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_subscription/finished_billing.html', context=None)

class PrivacyView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_subscription/privacy.html', context=None)

class TermsView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_subscription/terms.html', context=None)

''' -----------------------------------------------------
            INTERFACES FOR JAVASCRIPT - FRONT END
----------------------------------------------------- '''
@csrf_exempt
def stripe_sub_setup(request):

    # Designed for get requests.
    if request.method != 'GET':
        return HttpResponse(status=404)

    return JsonResponse({
        'publishableKey': STRIPE_PUBLIC_KEY,
        'basicPrice': 'price_1IXkXPLnm61uJv5f8369c8Wl',
        'proPrice': 'price_1IXkYoLnm61uJv5fvwF7oxzM'
    })

@csrf_exempt
def create_checkout_session(request):

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    data = json.loads(str(request.body, encoding='utf-8'))

    try:
        # See https://stripe.com/docs/api/checkout/sessions/create
        # for additional parameters to pass.
        # {CHECKOUT_SESSION_ID} is a string literal; do not change it!
        # the actual Session ID is returned in the query parameter when your customer
        # is redirected to the success page.
        checkout_session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse('stripe_sub_success')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('stripe_sub_cancel')),
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": data['priceId'],
                    # For metered billing, do not pass quantity
                    "quantity": 1
                }
            ],
        )
        return JsonResponse({'sessionId':checkout_session['id']})
    except Exception as e:
        return JsonResponse({'error': {'message': str(e)}}, status=400)

''' -----------------------------------------------------
        INTERFACES FOR JAVASCRIPT - SUCCESS - EDIT ACCOUNT
----------------------------------------------------- '''
@csrf_exempt
def checkout_session(request, **kwargs):

    # Designed for get requests.
    if request.method != 'GET':
        return HttpResponse(status=404)

    # Get the session_id passed in from create_checkout_session
    session_id = kwargs['session_id']
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    return JsonResponse(checkout_session)

@csrf_exempt
def customer_portal(request):

    # Designed for post requests.
    if request.method != 'POST':
        return HttpResponse(status=404)

    data = json.loads(str(request.body, encoding='utf-8'))
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.

    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = data['sessionId']
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = request.build_absolute_uri(reverse('stripe_sub_finished_billing'))

    session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url)
    return JsonResponse({'url': session.url})

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

    if event_type == 'checkout.session.completed':
        # Payment is successful and the subscription is created.
        # You should provision the subscription.
        print('\n')
        print('*'*20)
        print("checkout.session.completed")
        print("You probably need to update the database to provision the data.")
        print('*'*20)
    elif event_type == 'invoice.paid':
        # Continue to provision the subscription as payments continue to be made.
        # Store the status in your database and check when a user accesses your service.
        # This approach helps you avoid hitting rate limits.
        print('\n')
        print('*'*20)
        print("invoice.paid")
        print("You probably need to update the database to continue to provision the data.")
        print('*'*20)
    elif event_type == 'invoice.payment_succeeded':
        # This was an event type that I didn't find in the docs and seems to get
        # called when a subscription is initiated.
        print('\n')
        print('*'*20)
        print("invoice.payment_succeeded")
        print("You probably need to update the database to continue to provision the data.")
        print('*'*20)
    elif event_type == 'invoice.payment_failed':
        # The payment failed or the customer does not have a valid payment method.
        # The subscription becomes past_due. Notify your customer and send them to the
        # customer portal to update their payment information.
        print('\n')
        print('*'*20)
        print("invoice.payment_failed")
        print("You probably need to notify the user and send them to the portal to update their payment information.")
        print('*'*20)
    elif event_type == 'customer.subscription.updated':
        # Customer has updated the subscription.   Check the following:
        # subscription.items.data[0].price, and then make suitable adjustments in the
        # database.   Also can check subscription.items.data[0].quantity to see if
        # quantity is changed.
        print('\n')
        print('*'*20)
        print("customer.subscription.updated")
        print("Change to the subscription.   Please make suitable database access adjustments")
        print('*'*20)
    elif event_type == 'customer.subscription.deleted':
        # Customer has cancelled the subscription.   Remove the customers access
        # to the product.
        # If you configure the portal to cancel subscriptions at the end of a
        # billing period, listen to the customer.subscription.updated event to
        # be notified of cancellations before they occur. If cancel_at_period_end
        # is true, the subscription will be canceled at the end of its billing period.
        # If a customer changes their mind, they can reactivate their subscription
        # prior to the end of the billing period. When they do this, a
        # customer.subscription.updated event is sent. Check that cancel_at_period_end
        # is false to confirm that they reactivated their subscription.
        print('\n')
        print('*'*20)
        print("customer.subscription.deleted")
        print("Please make suitable database access adjustments")
        print('*'*20)
    else:
        print('\nUnhandled event type {}'.format(event_type))

    return JsonResponse({'status': 'success'})
