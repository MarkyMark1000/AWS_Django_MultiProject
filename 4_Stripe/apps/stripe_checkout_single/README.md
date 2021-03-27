
# OVERVIEW

This contains my notes on the Stripe Checkout setup which is contained within this app.
  
I believe that the Stripe Tutorials focus largely on the following paths:  
  * 1) Single Payment on pre-built Stripe Checkout page.  
  * 2) Single Payment using a custom page and Stripe Elements.  
  * 3) Subscription using pre-built Stripe Checkout page.  
  * 4) Subscription using a custom page and Stripe Elements.  
  
This App focuses on path 1 and is based on the following tutorial:
  
> https://stripe.com/docs/payments/accept-a-payment?integration=checkout&ui=checkout#auth-and-capture

I believe that this is the easiest system to setup.   You click a button that you setup in the webpage that takes you to the stripe website where the user pays for the desired item.   After completion, the page is redirected to your success or cancel pages.   A webhook is also called to indicate the success of the payment.

There is a section called Stripe Website References within this doc that explains what tutorials and information this is based upon.

### SETUP

---

* You need to have an account setup in the stripe dashboard.
* This system uses the public and private key's that you get for the Account on the Stripe Dashboard.   A file called 'hidden_account.py' needs to be created within the stripe_checkout_single directory.   This file is hidden from github, so may not exist.   It needs the following format:
    ```python
    # This key is used on the Client within the javascript
    STRIPE_PUBLIC_KEY = "..."
    # This key is used on the Server with the stripe library
    STRIPE_PRIVATE_KEY = "..."
    # Webhook Secret used when webhook is called.
    STRIPE_WEBHOOK_SECRET = "..."
    ```
* You may need to make some adjustments to the following section of code to define what you are purchasing.   Please see the section on 'CUSTOMIZING STRIPE AND THE CHECKOUT' and the comment in the code here:  
    ```views.py => CreateCheckoutSessionView```
* After the completion of a payment, Stripe sends the browser to either the success or cancel page.   However it also calls a webhook to allow the server to update.    To be able to replicate this webhook, the following needs to be done:
    * Install the stripe command line interface
    * Run the following command in a terminal:  
        ```stripe listen --forward-to localhost:8080/webhook/```
    * You need to get the webhook signing secret and update the 'hidden_account.py' file.
    * Then run this django project using the normal procedure.

### OUTPUT

---

When running succesfully, you should get an output printed to the terminal where Django is run which is similar to:

```
**********
Fulfilling order, please do not forget to update the code to do the following:
 - Save a copy of the order to your own database
 - Send the customer a receipt email
 - Reconcile line items and quantity purchased
**********
```

In production, you would need to update this code to take appropriate actions.

### SOME USEFUL COMMANDS

---

* login and pair with stripe account:
    > stripe login

* check status of the services:
    > stripe status

### CUSTOMIZING STRIPE AND THE CHECKOUT

---

It is possible to pre-build a Product or even a Customer in the stripe dashboard.    This means that when you check out it can have a pre-defined price and image and descriptions to help define what they are buying.    I suspect pre-defining cusomters is less useful unless you do it programatically and it is  used with subscriptions.   To define a Product in the dashboard go here:

> dashboard =>  products

You should then be able to add a product with images and prices etc.   Get the product 'ID' value and then update the code within ```views.py => CreateCheckoutSessionView``` to contain the code adjustment:

```python
line_items=[{
            'price': 'price_1IX31iLnm61uJv5fbtRJT3sl',
            'quantity': 1,
        }],
```

Here are some other adjustments that could be made to that section of code that may be interesting:

* Pre-fill Email address:  

    ```
    customer_email='mark_john_wilson@yahoo.co.uk',
    payment_method ........
    ```

* Change the checkout button text:  

    ```
    submit_type='donate',
    ```

* You can ask for shipping addresses to be collected:

    ```
    shipping_address_collection={
        'allowed_countries': ['US', 'CA'],
    },
    ```

You can customize the look of  the checkout using the stripe dashboard by going here:

> Stripe dashboard => settings => Branding


You can customize public facing information such as:  
* Return Policy  
* Support phone number, email and website  
* Links to terms of service and privacy policy  

### MOVING INTO PRODUCTION

---

* You need to get live values for STRIPE_PUBLIC_KEY, STRIPE_PRIVATE_KEY and STRIPE_WEBHOOK_SECRET and update the code appropriately.
* Webhooks - Stripe supports two endpoint types, Account and Connect. Create an endpoint for Account unless you’ve created a Connect application.
* Make the appropriate code changes mentioned in the 'OUTPUT' section.  

Please note that I have not currently tested this in production, so furthur unexpected adjustments could be required.

### STRIPE WESITE REFERENCES

---

This app is based largely upo the 'Accept a payment' section of the following page using the 'Prebuilt checkout page':

> https://stripe.com/docs/payments/accept-a-payment?integration=checkout&ui=checkout#auth-and-capture

To install the stripe command line interface:

> https://stripe.com/docs/stripe-cli#install

To customize the checkout experience:

> https://stripe.com/docs/payments/checkout/customization

To customize your success page to display customer information:

> https://stripe.com/docs/payments/checkout/custom-success-page
