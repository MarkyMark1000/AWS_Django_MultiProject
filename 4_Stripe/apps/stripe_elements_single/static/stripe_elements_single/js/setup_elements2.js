/**************************************************************
 setupElements FUNCTION, used in checkout.html javascript(footer)
                It gets the publishable key, creates a format
                for the stripe payment elements (card number etc)
                and then creates the 'stripe' payment fields within
                your form by mounting the 'card' onto your
                "#card-element" within the form.
**************************************************************/

var setupElements = function(data) {

    // KEY: stripe variable is defined and setup within checkout.html
    
    var elements = stripe.elements({
        fonts: [
          {
            cssSrc: 'https://fonts.googleapis.com/css?family=Quicksand',
          },
        ],
        // Stripe's examples are localized to specific languages, but if
        // you wish to have Elements automatically detect your user's locale,
        // use `locale: 'auto'` instead.
        locale: 'auto',
      });

    /*-------------------------------------------------------
    THESE ARE STRIPE SPECIFIC FORMATS BUILT WITH JAVASCRIPT.
    THIS GOES HAND IN HAND WITH THE setup_elements2.css SHEET.
    IT IS USED TO FORMAT STRIPE SPECIFIC ELEMENTS SUCH AS
    CARD NUMBER.
    -------------------------------------------------------*/
    var elementStyles = {
        base: {
          color: '#AAAAAA',
          fontWeight: 600,
          fontFamily: 'Quicksand, sans-serif',
          fontSize: '16px',
    
          ':-webkit-autofill': {
            color: '#AAAAAA',
          },
          ':focus': {
            color: '#AAAAAA',
          },
          '::placeholder': {
            color: '#AAAAAA',
          },
          ':focus::placeholder': {
            color: '#AAAAAA',
          },
        },
        invalid: {
          color: '#AAAAAA',
          ':focus': {
            color: '#FA755A',
          },
          '::placeholder': {
            color: '#FFCCA5',
          },
        },
    };
    
    var elementClasses = {
        focus: 'focus',
        empty: 'empty',
        invalid: 'invalid',
    };
  
    // Create the 'stripe' card and then mount it onto the div
    // "#card-element" within the form.
    /*  GET RID OF THIS:
    var card = elements.create("card", { style: style });
    card.mount("#card-element");
    */

    var cardNumber = elements.create('cardNumber', {
      style: elementStyles,
      classes: elementClasses,
    });
    cardNumber.mount('#example3-card-number');

    var cardExpiry = elements.create('cardExpiry', {
        style: elementStyles,
        classes: elementClasses,
    });
    cardExpiry.mount('#example3-card-expiry');

    var cardCvc = elements.create('cardCvc', {
        style: elementStyles,
        classes: elementClasses,
    });
    cardCvc.mount('#example3-card-cvc');

    return {
      stripe: stripe,
      cardNumber: cardNumber,
      cardExpiry: cardExpiry,
      cardCvc: cardCvc,
      clientSecret: data.clientSecret
    };

};