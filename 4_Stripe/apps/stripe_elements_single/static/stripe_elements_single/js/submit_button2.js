/**************************************************************
 pay FUNCTION, used in initial setup
     Calls stripe.confirmCardPayment which creates a pop-up modal to
     prompt the user to enter extra authentication details without
     leaving your page
**************************************************************/
var pay = function(stripe, cardNumber, cardExpiry, cardCvc, clientSecret) {

    // cardExpiry is not currently used.   I have emailed stripe asking how
    // to use this with confirmCardPayment and may adjust the code when they
    // get back.

    // Function Below  - disable button, show spinner etc.
    changeLoadingState(true);

    // Gather additional customer data we may have collected in our form.
    var form = document.querySelector('form');
    var name = form.querySelector('#example3-name');
    var zip = form.querySelector('#example3-zip');
    var email = form.querySelector('#example3-email');
    var billingData = {
        name: name ? name.value : undefined,
        address: { postal_code: zip ? zip.value : undefined },
    };

    // Initiate the payment.
    // If authentication is required, confirmCardPayment will automatically display a modal

    stripe
        .confirmCardPayment(clientSecret, {
        payment_method: {
            card: cardNumber,
            billing_details: billingData,
        },
        receipt_email: email,
        })
        .then(function(result) {
        if (result.error) {
            // Show error to your customer
            showError(result.error.message);
        } else {
            // The payment has been processed!
            orderComplete(clientSecret);
        }
        });
};

/**************************************************************
 POST-PAYMENT Helper Functions
**************************************************************/

/*-------------------------------------------------------------
Function: orderComplete, used in pay above when submit results in
          a successful payment.
-------------------------------------------------------------*/
var orderComplete = function(clientSecret) {
    // Just for the purpose of the sample, show the PaymentIntent response object
    stripe.retrievePaymentIntent(clientSecret).then(function(result) {
        var paymentIntent = result.paymentIntent;
        var paymentIntentJson = JSON.stringify(paymentIntent, null, 2);

        document.querySelector(".sr-payment-form").classList.add("d-none");
        document.querySelector("pre").textContent = paymentIntentJson;

        document.querySelector(".sr-result").classList.remove("d-none");

        setTimeout(function() {
        document.querySelector(".sr-result").classList.add("expand");
        }, 200);

        changeLoadingState(false);
    });
};

/*-------------------------------------------------------------
Function: showError, used in pay above when an error is
          encountered.
-------------------------------------------------------------*/
var showError = function(errorMsgText) {

    changeLoadingState(false);

    var errorMsg = document.querySelector(".sr-field-error");
    errorMsg.textContent = errorMsgText;

    setTimeout(function() {
        errorMsg.textContent = "";
    }, 4000);

};
  
/*-------------------------------------------------------------
Function: changeLoadingState, used in pay above
-------------------------------------------------------------*/
var changeLoadingState = function(isLoading) {
    if (isLoading) {
        document.querySelector("button").disabled = true;
        document.querySelector("#submit-spinner").classList.remove("d-none");
        document.querySelector("#button-text").classList.add("d-none");
    } else {
        document.querySelector("button").disabled = false;
        document.querySelector("#submit-spinner").classList.add("d-none");
        document.querySelector("#button-text").classList.remove("d-none");
    }
};
