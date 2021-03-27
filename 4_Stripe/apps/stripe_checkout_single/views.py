from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import stripe
from apps.stripe_checkout_single.hidden_account import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, \
                           STRIPE_WEBHOOK_SECRET

# IMPORTANT - INITIATE stripe WITH SECRET KEY
stripe.api_key = STRIPE_SECRET_KEY

''' -----------------------------------------------------
                PUBLIC FACING VIEWS
----------------------------------------------------- '''

class TestDataView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_single/test_data.html', context=None)

class SuccessView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_single/success.html', context=None)

class CancelView(View):

    def get(self, request, **kwargs):

        return render(request, 'stripe_checkout_single/cancel.html', context=None)


class BasicView(View):

    def get(self, request, **kwargs):

        context = {
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY
        }

        return render(request, 'stripe_checkout_single/basic.html', context=context)

''' -----------------------------------------------------
                CREATE CHECKOUT AND ID CODE
----------------------------------------------------- '''
# class CreateCheckoutSessionView(View):
@csrf_exempt
def checkout_session_view(request):

  """
  Original line_items:
  line_items=[{
      'price_data': {
          'currency': 'gbp',
          'product_data': {
          'name': 'T-shirt',
          },
          'unit_amount': 2000,
      },
      'quantity': 1,
      }],
  """

  # Adjusted code that uses a product defined in stripe dashboard:
  session = stripe.checkout.Session.create(
      customer_email='mark_john_wilson@yahoo.co.uk',
      payment_method_types=['card'],
      line_items=[{
      'price': 'price_1IX31iLnm61uJv5fbtRJT3sl',
      'quantity': 1,
      }],
      mode='payment',
      success_url = request.build_absolute_uri(reverse('stripe_success')+'?session_id={CHECKOUT_SESSION_ID}'),
      cancel_url = request.build_absolute_uri(reverse('stripe_cancel')),
  )

  return JsonResponse({'id':session.id})

''' -----------------------------------------------------
                    WEB HOOK CODE
----------------------------------------------------- '''
@csrf_exempt
def my_webhook_view(request):

  '''
  The following code verifies that the webhook is received from stripe
  and then raises errors if it is not.
  It is based on code from the following location:
  https://stripe.com/docs/payments/checkout/fulfill-orders
  '''

  # Extract Data from Webhook
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  # Test to ensure the webhook came from stripe
  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, STRIPE_WEBHOOK_SECRET
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # If from stripe, handle the checkout
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Fulfill the purchase
    fulfill_order(session)

  # Passed signature verification
  return HttpResponse(status=200)

def fulfill_order(session):
    '''
    Here are some suggestions on fulfilling the order:
        - Saving a copy of the order in your own database.
        - Sending the customer a receipt email.
        - Reconciling the line items and quantity purchased by the customer if using line_item.adjustable_quantity.
    
    Use dir to explore the structure of session and payload.
    '''
    print('\n')
    print('*'*10)
    print('stripe_checkout_single:')
    print("Fulfilling order, please do not forget to update the code to do the following:")
    print(" - Save a copy of the order to your own database")
    print(" - Send the customer a receipt email")
    print(" - Reconcile line items and quantity purchased")

    print('*'*10)