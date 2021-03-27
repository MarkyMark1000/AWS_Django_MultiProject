# OVERVIEW

This project was designed to investigate the use of PayPal.

I should warn you that the project was abandoned after a short period of time, but I have kept it within the project list as a useful reminder.

It is relatively simple to add some basic paypal buttons to a site, however I started to encounter problems when adding advanced payment options into a webpage.

I have left this project in because at some point in the future, I would like to go through paypal and investigate it furthur, but this has become a low priority at present because I have been using stripe.

### SETUP

---

This project is dependent upon a file that stores the sandbox account information.   This is not included in github and is stored in the following location:

> apps/paypal_templates/extra_code_or_config/paypal_account.py

The file will need to contain contents similar to the following:

```python
'''
THIS FILE SHOULD BE HIDDEN FROM GITHUB UNLESS IT IS A PRIVATE ACCOUNT  
TO AVOID SECRET DATA BEING REVEALED.

IT STORES SECURITY CONSTANTS FOR PAYPAL

'''

# PAYPAL CONSTANTS
SANDBOX_ACCOUNT = "sb-wc37iu5397280@business.example.com"
SANDBOX_CLIENT_ID = "..............."
SANDBOX_SECRET = "................"
SANDBOX_CURRENCY = "GBP"
SANDBOX_LOCALE = "en_GB"
SANDBOX_BASE_URL = "https://api-m.sandbox.paypal.com/"

# SANDBOX ACCOUNT INFORMATION
SANDBOX_PERSONAL_ACCOUNT_NAME = "sb-ov7i05393887@personal.example.com"
SANDBOX_PERSONAL_FIRST_NAME = "john"
SANDBOX_PERSONAL_LAST_NAME = "doe"
SANDBOX_PERSONAL_EMAIL = "sb-ov7i05393887@personal.example.com"
SANDBOX_PERSONAL_PASSWORD = "........"

SANDBOX_BUSINESS_ACCOUNT_NAME = "sb-wc37iu5397280@business.example.com"
SANDBOX_BUSINESS_FIRST_NAME = "John"
SANDBOX_BUSINESS_LAST_NAME = "Doe"
SANDBOX_BUSINESS_EMAIL = "sb-wc37iu5397280@business.example.com"
SANDBOX_BUSINESS_PASSWORD = "......."

# LIVE ACCOUNT INFORMATION
LIVE_ACCOUNT = "......"
LIVE_CLIENT_ID = "........."
LIVE_SECRET = "............"
LIVE_CURRENCY = "GBP"
LIVE_LOCALE = "en_GB"
LIVE_BASE_URL = "https://api-m.paypal.com/"
```