
/**************************************************************
 pay FUNCTION, used in initial setup
     Calls stripe.confirmCardPayment which creates a pop-up modal to
     prompt the user to enter extra authentication details without
     leaving your page
**************************************************************/
var pay = function(stripe, card, clientSecret) {

    // Function Below  - disable button, show spinner etc.
    changeLoadingState(true);

    // I PROBABLY WANT TO ADJUST THE FOLLOWING BIT TO INCLUDE POSTCODE ETC.

    // Initiate the payment.
    // If authentication is required, confirmCardPayment will automatically display a modal
    stripe
        .confirmCardPayment(clientSecret, {
        payment_method: {
            card: card
        }
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