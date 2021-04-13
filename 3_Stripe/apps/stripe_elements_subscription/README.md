# OVERVIEW

This contains my notes on the Stripe Elements setup which is contained within this app.
  
I believe that the Stripe Tutorials focus largely on the following paths:  
  * 1) Single Payment on pre-built Stripe Checkout page.  
  * 2) Single Payment using a custom page and Stripe Elements.  
  * 3) Subscription using pre-built Stripe Checkout page.  
  * 4) Subscription using a custom page and Stripe Elements.  
  
This App focuses on path 4 and is based on the following tutorial:
  
> https://stripe.com/docs/billing/subscriptions/fixed-price

Before I start, I would like to highlight that I found some problems with this tutorial.   I have written to stripe, so this issue may be resolved in the near future, but if you look at the code on the website and compare it to the code within their github library, you will see that they are not the same.   In particular I noticed the following point:  
    - The webpage references a file called script.js and a function called createCustomer.  
    - If you follow the link on the page to the github library, you will find that there is no script.js file.

For this reason, I have made the most out of the github library that is present to create this app.

Github library:
> https://github.com/stripe-samples/subscription-use-cases/tree/master/fixed-price-subscriptions

In a similar manner to stripe_elements_single, this uses javascript to embed stripe payment elements such as the card numer into a form, however it is much more involved because you need to create an account, choose a subscription plan and allow for subscriptions to be cancelled.

I also feel that to really make use of this project, it would need to be incorporated into an account system, with the webhooks providing access to some kind of programming feature or regular delivery.   To  keep things simple, I have not tried this here and have concentrated on learning how the stripe code works and incorporating it into my own site.

With respect to formatting, it is worth remembering that certain fields such as the card number are built in javascript and are seperate:
   - You can format elements that are within the form, but not used for payment using standard csv.
   - For elements that are part of the stripe payment system, such as the card number, expiry and c2v, you can format the fields by editing the javascript.
   - There is also a custom css file, which contains css to format the payment form.   This contains classes such as 'StripeElement' which are applied after the custom stripe fields such as card number are built.   Use this in combination with the previous 2 points to format the form.
   - The css formating uses some imported fonts at the top of the file.

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
* You may need to make some adjustments to the price or code that generates a price for the payment intent: 
    > views.py => create_subscription_view
    > es_prices.html
* The system uses a webhook again, so to replicate this webhook, the following needs to be done:
    * Install the stripe command line interface
    * Run the following command in a terminal:  
        ```stripe listen --forward-to localhost:8080/stripe_elements_sub_webhook/```
    * You need to get the webhook signing secret and update the 'hidden_account.py' file.
    * Then run this django project using the normal procedure.

### OUTPUT

---

When running succesfully, you should get an output printed to the terminal where Django is run which is similar to:

```
********************
Webhook:
********************
invoice.paid
......
********************
```

In production, you would need to update this code to take appropriate actions on your system.

### SOME USEFUL COMMANDS

---

* login and pair with stripe account:
    > stripe login

* check status of the services:
    > stripe status

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
