/**************************************************************
 setupElements FUNCTION, used in checkout.html javascript(footer)
                It gets the publishable key, creates a format
                for the stripe payment elements (card number etc)
                and then creates the 'stripe' payment fields within
                your form by mounting the 'card' onto your
                "#card-element" within the form.
**************************************************************/

var setupElements = function(stripe) {

  // KEY: stripe variable is defined and setup within checkout.html

  var elements = stripe.elements();

  // define style to be used within the stripe payment
  // elements (card numer etc)
  var style = {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4"
      }
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a"
    }
  };

  // Create the 'stripe' card and then mount it onto the div
  // "#card-element" within the form.
  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  return {
    stripe: stripe,
    card: card
  };
};