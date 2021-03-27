from django.shortcuts import render
from django.views import View
from apps.paypal_templates.extra_code_or_config.paypal_environment import \
    PAYPAL_ACCOUNT, PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_IS_LIVE, \
    PAYPAL_LOGIN_DATA, PAYPAL_CURRENCY, PAYPAL_LOCALE, PAYPAL_BASE_URL
import requests
import datetime as dt

class PayPalAuthenticationToken():
    """
    IMPORTANT:
    Update the Accept-language
    Update the url based upon sandbox

    """

    def __init__(self):
        self.client_access_token = None
        self.client_start_time = None
        self.client_expiry_time = None

    def _extract_expiry(self, nonce, expires_in):
        """
        given a string like this, we need to build a date:
        2021-03-13T17:16:02ZD5NMIrjBAD7mxmEiRwlTnIwTk8UeuBCtZuG3UBpMXhA
        then add expires_in onto this to get the expiry date.

        Data is returned as a dictionary:
        {'valid': True, 'start_time': ..., 'expiry_time': ...}

        if successful, we can use time to validate the client_access_token
        or a 404 error, if unsuccessful, then we need to use 404 errors.
        """

        try:

            #Extract date and time string
            first_colon = nonce.index(":")
            second_colon = nonce.index(":",first_colon+1)
            date_time_string = nonce[:second_colon+3]

            # Convert it to a date
            dt_start = dt.datetime.strptime(date_time_string,
                                           "%Y-%m-%dT%H:%M:%S")

            # Add the expiry in seconds (minus 1 second)
            delta = dt.timedelta(seconds=int(expires_in)-1)

            # Get the expiry
            dt_expiry = dt_start + delta

            # Return the time
            return dt_start, dt_expiry

        except:
            # Error, cannot use expiry
            return None, None

    def _extract_client_token_and_expiry(self):
        """
        This is used to extract client token information in a similar manner to
        the following page:
        https://developer.paypal.com/docs/api/get-an-access-token-curl/
        """

        # Data to pass into requests
        # url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        url = PAYPAL_BASE_URL + "/v1/oauth2/token"
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET)
        headers = {
            "Accept": "application/json",
            "Accept-Language": PAYPAL_LOCALE,
        }
        data = {
            "grant_type": "client_credentials"
        }

        # Request client token
        r = requests.post(url=url, headers=headers, auth=auth, data=data)

        # Process the request
        if r.status_code == 200:
            # Successful response
            json_data = r.json()
            dict_data = dict(json_data)
            
            # Populate the results into class variables
            self.client_access_token = dict_data['access_token']

            self.client_start_time, self.client_expiry_time = \
                self._extract_expiry(dict_data['nonce'],
                                     dict_data['expires_in'])

        else:
            # Set the data to None
            self.client_access_token, self.client_start_time, \
            self.client_expiry_time = None, None, None

    def _extract_page_token_and_expiry(self, try_again=True):
        """
        This is used to extract client token information in a similar manner to
        the following page:
        https://developer.paypal.com/docs/business/checkout/advanced-card-payments/
        """

        # Data to pass into requests
        # url = "https://api-m.sandbox.paypal.com/v1/identity/generate-token"
        url = PAYPAL_BASE_URL + "v1/identity/generate-token"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer { self.client_access_token }',
            'Accept-Language': PAYPAL_LOCALE
        }

        # Request client token
        r = requests.post(url=url, headers=headers)

        # Process the request
        if r.status_code == 200:

            # Successful response
            json_data = r.json()
            dict_data = dict(json_data)
            
            return dict_data['client_token']

        elif r.status_code == 401 and try_again:

            # 401 error, try refreshing the client token, then try to
            # get the page token one more time

            self._extract_client_token_and_expiry()

            return self._extract_page_token_and_expiry(try_again=False)

        else:

            raise ValueError('Could not extract page access token')

    def get_page_access_token(self):
        """
        Check the client access token and potentially refresh it.

        Then use the client acces token to get the token used in
        the website page
        """

        # If there is no data, refresh the token
        if self.client_access_token is None or self.client_expiry_time is None:
            self._extract_client_token_and_expiry()
        
        # If the token has expired, refresh it
        if self.client_expiry_time is not None:
            if dt.datetime.now() >= self.client_expiry_time:
                self._extract_client_token_and_expiry()
        
        # Attempt to use the access token to get he page access token.
        return self._extract_page_token_and_expiry()

G_AUTHENTICATION = PayPalAuthenticationToken()

class SandboxView(View):

    def get(self, request, **kwargs):

        # This view displays the sandbox data

        context = {
            'PAYPAL_IS_LIVE': PAYPAL_IS_LIVE,
            # Add the sandbox login data
            'LOGIN_DATA': PAYPAL_LOGIN_DATA,
        }

        return render(request, 'paypal_templates/sandbox.html', context=context)

class VeryBasicView(View):

    def get(self, request, **kwargs):

        # This view is based upon the following paypal information:
        # https://developer.paypal.com/docs/business/checkout/set-up-standard-payments/
        # https://www.paypal.com/buttons/smart?flowloggingId=004609ba385e1

        context = {
            'CLIENT_ID': PAYPAL_CLIENT_ID,
            'CURRENCY': PAYPAL_CURRENCY,
            'LOCALE': PAYPAL_LOCALE,
            'AMOUNT': 12,
            'PAYPAL_IS_LIVE': PAYPAL_IS_LIVE,
            # Add the sandbox login data
            'LOGIN_DATA': PAYPAL_LOGIN_DATA,
        }

        return render(request, 'paypal_templates/very_basic.html', context=context)

class SuccessView(View):

    def get(self, request, **kwargs):

        # Basic Review to report that a payment has been successful

        return render(request, 'paypal_templates/success.html', context=None)
