# EXTRA NOTES:

---

This section covers 3D secure and the changes required:

https://www.paypal.com/uk/webapps/mpp/psd2

Apparently you can force your account to become 3D secure.

Check the section on 'PayPal Pro Hosted' and 'PayPal Pro Direct'

### WEBHOOKS

---

There is a whole section on webhooks here:
https://developer.paypal.com/docs/api-basics/notifications/webhooks/

There is stuff mixed in with alternative payment methods on this page:
https://developer.paypal.com/docs/business/checkout/configure-payments/alternative-payment-methods/


https://developer.paypal.com/docs/api/webhooks/v1/

### ADD CAPABILITIES

---

This is based upon the following section:

> https://developer.paypal.com/docs/business/checkout/add-capabilities/

- It is possible to create an authorise and capture system, where the payment
is authorised, then you check the stock and then finally you capture the payment
if something is in stock.

- It mentions about improving the buyer experience.   This might be useful, especially the section on handling errors.

    > https://developer.paypal.com/docs/business/checkout/add-capabilities/buyer-experience/

- It looks like there is a section on SCA (Strong Customer Authentication) and it looks like it is only applicable to 'Advanced Credit and Debit Card Payments'.

- It also looks like there is a fraud protection section for 'advanced card processing', to help avoid bad payments.

### 3D Secure

---

There is a section on 3D Secure here:

https://developer.paypal.com/docs/business/checkout/3d-secure/3d-secure-sdk/

I suspect that we only need to make adjustments if we are making  'advanced card processing'.

It looks like there is a LiabilityShift field that can switch from the merchant to the card issuer etc.

There are a set of card and input values that you can use to test 3D Secure.   I am not sure if this works in the AWS Standard Input, but could be useful if you try 'advanced card processing':
https://developer.paypal.com/docs/business/checkout/3d-secure/3d-secure-test/

### FORMATTING

---

There are some interesting formatting description's here:
> https://developer.paypal.com/docs/business/checkout/reference/style-guide/

Please note the option to style.tagline to false to disable the tagline text.

### Popup blockers

---

The checkout experience is designed to launch in a popup window. The payment buttons continue to work if popup blockers are active. However, PayPal recommends that you do not use popup blockers with this integration.

### Internet Explorer and Edge Problems

---

See the very bottom of this page:

> https://developer.paypal.com/docs/business/checkout/reference/browser-support/

### CARD ERROR CODES

---

https://developer.paypal.com/docs/business/checkout/reference/card-decline-errors/

# PERSONAL QUESTIONS / NOTES

---

In the basic/standard system, is it possible to switch off the 'Deliver to billing address' option because this just isn't relevant to me.

I have been getting some crummy response with the Debit or Credit Card option on the basic integration.   Test and try this out more.

### PAYMENT DATA TRANSFER

---

I found the following link that may be useful for confirming purchases:

> https://developer.paypal.com/docs/api-basics/notifications/payment-data-transfer/