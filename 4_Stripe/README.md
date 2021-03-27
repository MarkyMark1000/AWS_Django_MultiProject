# OVERVIEW

This project displays a set of pages for trying out stripe payments.

Initially, I tried using paypal for a checkout, but hit a couple of problems.   While waiting for a response, I sent an email to multiple payment gateway providers pointing out that I wanted a system that could do individual payments and subscriptions.

At this moment, roughly 2 weeks since my initial email, stripe was the only one to get back to me.   I was sent lots of links highligting the information that I was interested in, which I will include at the end of this document.   If you want to use stripe, I suggest you send an email to one of their sales people.   It has been my experience that they get back quite quickly with some good information.   The Python code that I looked at initially was good quality and I have found it relatively easy to understand their code, however I do think you need to have a basic, but solid understanding of Flask and Django (this system uses Django).

After a bit of research, I found that there are roughly 2 areas that were relevant in stripe:
* Checkout - a simpler method, where stripe provides the payment form.
* Stripe Elements - more complicated, but allows you to embed forms within your website.

This project has an apps directory with multiple apps within it.   At present, only two of the following plans have been completed, but I am planning to create an app for each of the following:
  * 1) Single Payment on pre-built Stripe Checkout page.  
  * 2) Single Payment using a custom page and Stripe Elements.  
  * 3) Subscription using pre-built Stripe Checkout page.  
  * 4) Subscription using a custom page and Stripe Elements.  

(Please note that there is some code repetition which may be a bit annoying, but I can live with this because I would never use all of these payment methods at the same time within a live website)

Each app has it's own README file which you need to read to get it's features up and running.

At present I have only got 1) and 3) working.

### Dependencies:

---

This project has some dependency on the stripe command line interface when running webhooks in development:

    > https://stripe.com/docs/stripe-cli#install

Useful commands are:

> stripe login              (login and pair with stripe account)

> stripe status             (check status of the services)

You can customize the look and feel of the 'CHECKOUT' within the stripe dashboard:

> Stripe dashboard => settings => Branding

You can customize public facing information such as:  
    - Return Policy  
    - Support phone number, email and website  
    - Links to terms of service and privacy policy  

### Github Examples that I believe are relevant:

---

1) Single Payment on pre-built Stripe Checkout page:
    > https://github.com/stripe-samples/checkout-one-time-payments/tree/master/client/html
    > https://github.com/stripe-samples/checkout-one-time-payments/blob/master/server/python/server.py
2) Single Payment using a custom page and Stripe Elements:
    > 
3) Subscription using pre-built Stripe Checkout page:
    > https://github.com/stripe-samples/checkout-single-subscription/tree/master/server/python
4) Subscription using a custom page and Stripe Elements:
    > 

### Email sent by Stripe:

---

Thank you for your interest in Stripe! I hope all is well with you and your team. First, we are truly grateful that you have considered Stripe as a payment gateway, we are excited to receive partners like you everyday.

STRIPE
For a bit of context, Stripe is a full stack solution that performs the functions of both a payment gateway and merchant account. With Stripe you can easily start accepting payments on your website and we pay out those funds into your bank. This significantly simplifies your operation and means that you can focus on what matters most for you: your customers.

https://stripe.com/payments

Our API can be used with different coding languages like Curl, Ruby, Java or Python. We also offer documentation for different coding languages which can be found here:

https://stripe.com/docs/api
https://github.com/stripe/stripe-python

Billing Feature: provides a fully-stacked subscription service for growing businesses. Our intuitive dashboard allows for structured creation of subscriptions using four principal features: Invoices, Subscriptions, Products and Coupons. I've given a brief outline of each of these below.

Invoices:
While invoices in Stripe have historically described the mechanism for recurring billing, you now have options when it comes to sending your customer an invoice! You can choose to continue sending an invoice as a part of your recurring billing model or you can send one-time invoices to charge your customers. Your customers will also have the ability to pay their emailed invoices directly on a Stripe-hosted payment page. Here, your customer will be able to pay their invoice via card. Stripe will automatically handle payment reconciliation, reducing manual work.

Subscriptions, Products
Here, you can 'attach' your customer to the desired subscription plan. It allows you to determine the structure of the subscription. When you have a customer created, you can select them, add a product (with a determined pricing plan), and control the subscription from here.

Coupons
If you wish to reward clients at any stage with a reduced price on a subscription, you can apply for a coupon. These coupons can be customised to deduct any percentage amount from the subscription.

I invite you to try all our features in test mode and be sure that we're the best fit for your business. Just follow the next steps to register, fill out the application form and get started:

1. https://dashboard.stripe.com/register

2. Learn more about our Stripe Dashboard

3. Test payments with us in the test view on our Stripe Dashboard

4. Integrate Stripe to your website

I really hope this gives you a better insight on how easy it is to work with us and for sure to get started. If you feel like you need more information on a specific product or still have some questions, please do not hesitate to contact me back, I’ll be here just one email away to help you.
