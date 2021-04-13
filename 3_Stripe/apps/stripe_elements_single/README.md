# OVERVIEW

This contains my notes on the Stripe Elements setup which is contained within this app.
  
I believe that the Stripe Tutorials focus largely on the following paths:  
  * 1) Single Payment on pre-built Stripe Checkout page.  
  * 2) Single Payment using a custom page and Stripe Elements.  
  * 3) Subscription using pre-built Stripe Checkout page.  
  * 4) Subscription using a custom page and Stripe Elements.  
  
This App focuses on path 2 and is based on the following tutorial:
  
> https://stripe.com/docs/payments/accept-a-payment?integration=checkout&ui=elements

Before I start, I would like to highlight that I found it easier to understand the tutorial if you just follow the 'view full sample' links to the code on github and then analyse it from there.

This system uses javascript to embed stripe payment elements such as the card number into a form.   There are two examples that come with this app:  
1 - One app displays the basic card form that contains the card number, card expiry, c2v and postcode within a single element.   This is relatively easy to setup.  
2 - I wanted to try out some other options.   The second example has custom formatting and a seperate card number.   This is a bit tricky and it is worth noting the following with respect for formatting:  
   - You can format elements that are within the form, but not used for payment using standard csv (I suggest the appropriate setup_elements file).
   - For elements that are part of the stripe payment system, such as the card number, expiry and c2v, you can format the fields by editing the javascript within the setup_elements/elements2.js module.
   - There is also a custom css file called setup_elements.css, which contains css to format the payment form.   This contains classes such as 'StripeElement' which are applied after the custom stripe fields such as card number are built.   Use this in combination with the previous 2 points to format the form.
   - The css formating uses some imported fonts at the top of the checkout.html files.
   
I have emailed stripe about this and at present I have not heard back, but the second example has the advantage of having more flexibility to format the form.   However it onlu uses the card number and not the expiry or ccv to validate the card, ie to me it looks slightly less secure.   Stripe may get back to me on this and tell me how to modify the code to cope with this situation.

I have attempted to break the javascript and css files into many bits to make it as readable as possible.   checkout/checkout_2.html is the core file that then calls setup_elements and submit_button respectively.

If you wish to enhance the format of the payment forms furthur, the following page contains some examples:

https://stripe.dev/elements-examples/

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
    ```urls.py => 'stripe_elements_create_payment_intent'```
* The system uses a webhook again, so to replicate this webhook, the following needs to be done:
    * Install the stripe command line interface
    * Run the following command in a terminal:  
        ```stripe listen --forward-to localhost:8080/stripe_elements_webhook/```
    * You need to get the webhook signing secret and update the 'hidden_account.py' file.
    * Then run this django project using the normal procedure.

### OUTPUT

---

When running succesfully, you should get an output printed to the terminal where Django is run which is similar to:

```
********************
Webhook:
********************
Payment received.
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
