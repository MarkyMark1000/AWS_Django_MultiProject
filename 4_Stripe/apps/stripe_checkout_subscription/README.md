# OVERVIEW

This contains my notes on the Stripe Checkout setup which is contained within this app.
  
I believe that the Stripe Tutorials focus largely on the following paths:  
  * 1) Single Payment on pre-built Stripe Checkout page.  
  * 2) Single Payment using a custom page and Stripe Elements.  
  * 3) Subscription using pre-built Stripe Checkout page.  
  * 4) Subscription using a custom page and Stripe Elements.  
  
This App focuses on path 3 and is based on the following tutorial:
  
> https://stripe.com/docs/billing/subscriptions/checkout

This tutorial is a bit more difficult to follow that that specified in the stripe_checkout_single app.   I found the tutorial a bit difficult to follow, however I found that you could 'View full sample' to see the full code.   This makes it much easier to follow and has missing bits of code that explain what is happening.

You can suscript to one of two payment options which have been setup previously in the stripe dashoard.   Upon successful subscription you go to a success page.   In this system the success page stores the customer id and has a button that lets the user alter their subscription.   In  a real project, you probably want to save the customer id with the users account and have a menu item to edit the subscription.
It also calls a number of webhook requests that let you know when the subscription changes.   In a real project, these would need to be adjusted to update the user access.

### CUSTOMER PORTAL

---

When dealing with subscriptions, there is a customer portal where customers can manage their subscriptions.

This video gives a demonstraton on customizing the portal:

> https://www.youtube.com/watch?v=u8H6awDJVpM

You can configure the client portal using the following  in the stripe dashboard:

> Stripe Dashboard => settings => Billing => Customer Portal
> Stripe Dashboard => settings => Billing => Subscriptions and Emails

A list of setting  options can be found on the tutorial page, they include:
* Update subscription pricing plans
* Update subscription quantities
* Cancel subscriptions
* Update payment methods
* View invoice history
* Update billing information
* Apply promotion codes

There are compulsory url's such as privacy_policy_url and terms_of_service_url that need to be created for this to work.

Product Catalog
If you allow customers to upgrade, downgrade, or change the quantities of their subscriptions, you must also set a product catalog. This includes the products and prices that your customers can upgrade or downgrade to, as well as the subscriptions on which they can update quantities.

Updating subscriptions in the portal is only supported for charge_automatically subscriptions with a single licensed price.

For example, these cannot be updated in the portal (but can be cancelled):  Multiple products, Metered billing, Non-card payment methods

BEWARE:
Subscriptions attached to schedules cannot be updated or canceled.

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
* When setting up the strip subscription on the stripe dashboard (settings => Billing => customer portal, settings => Billing => Subscriptions and Emails), you need to have a website reference for terms and conditions and privacy.   These views and templates exist within the views.py file, but will need updating.
* There are largely 4 area's of code in the views.py file:
    * A section for simple views like terms and conditions, privacy, success etc.
    * A section of code that represents javascript interfaces for the front end, ie where the initial subscription is made.
    * A section of code that represents javascript interfaces for the success page where the user can edit their subscription.   As mentioned previously, in a real project, you would probably want to save the customer id and have a different method of editing the account.
    * A section of code for webhooks that are passed to the server when the customer subscribes or changes his subscription.   This would need to be edited to update the database appropriately in a live project.
* In the stripe dashboard, navigate to the Create a product page, and create two products. Add one price for each product, each with a monthly billing interval:
    > Basic option—Price 5.00 GBP  
    > Premium option—Price 15.00 GBP  
* After you create the prices, record the price IDs so you can use them in subsequent steps.   My price id's were:
    > prod_JA4gqzFjj6a1Jg  
    > prod_JA4iqigUdBF8h2
* The following view uses the price id's for the subscriptions that are created using the stripe dashboard, so this will need to be updated:
    * stripe_sub_setup
* This system is dependent upon stripe being setup in the requirements file and the stripe command line interface being setup.   You need to run ```stripe login``` to pair the cli with a stripe account.
* To replicate how the webhook works for this project, you will need to use the stripe command line interface.   Please note that this line of code is different to the other app's.   I have tried to make each app independent:
    * Install the stripe command line interface
    * Run the following command in a seperate terminal to the webserver:
        ```stripe listen --forward-to localhost:8080/stripe_sub_webhook/```
    * You need to get the webhook signing secret and update the 'hidden_account.py' file.
    * Then run this django project using the normal procedure.

### MOVING INTO PRODUCTION

---

* You need to get live values for STRIPE_PUBLIC_KEY, STRIPE_PRIVATE_KEY and STRIPE_WEBHOOK_SECRET and update the code appropriately.
* You would need to update the price codes of the subscriptions that you are selling within the following view:
    * stripe_sub_setup
    * (NOTE:  THERE IS A 'COPY TO LIVE MODE' BUTTON AT THE TOP SHOULD YOU WISH TO MOVE TO A LIVE ACCOUNT.)
* Code adjustments to display appropriate buttons, icons and javascript calls would need to be made if you increase or decrease the number of subscriptions.   See the html and javascript code in the followint template:
    * basic.html
* Webhooks - Adjust the webhooks to update a live database as the user subscribes or makes changes to their subscripiton.
* You probably want to save a customer id in the database and adjust how the user accesses and adjusts their subscription, instead of using the success.html page. 

Please note that I have not currently tested this in production, so furthur unexpected adjustments could be required.

### OUTPUT

---

When running succesfully, you should get an output printed to the terminal where Django is run.   It will print out some lines indicating that certain events are 'Unhandled'.   You could adjust the code to handle the event, but it also displays some lines similar to the following (it could be mingled with unhandled events):

```
********************
customer.subscription.deleted
Please make suitable database access adjustments
********************
```

In production, you would need to update this code to adjust the database appropriately.

### TESTING

As you configure the settings, you can preview the portal by clicking the Preview button.

After saving the settings, you can launch the portal and test it using a customer in test mode. Navigate to a customer in the Dashboard and then click the Actions button and select Open customer portal.

Check the subscriptions and updates to the subscription within the stripe dashboard.

### STRIPE WESITE REFERENCES

---

This app is based largely upon the 'Create subscriptions with Checkout' tutorial.   Please note that I believe the tutorial is a bit unclear.   If you use the 'View full sample' buttons you can see all of the code and it is much easier to understand:

> https://stripe.com/docs/billing/subscriptions/checkout

To install the stripe command line interface:

> https://stripe.com/docs/stripe-cli#install
