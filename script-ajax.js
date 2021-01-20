const button = document.querySelector('#buy_now_btn');

button.addEventListener('click', event => {
    var name = document.getElementsByName('name')[0].value
    var amount = document.getElementsByName('amount')[0].value
    // alert(JSON.stringify(document.getElementsByName('name')))
    fetch('/home/', {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },

        //make sure to serialize your JSON body
        body: JSON.stringify({
            name: name,
            amount: amount
        })
    })
        .then((result) => {
            return result.json();
        })
        .then((data) => {
            var stripe = Stripe(data.checkout_public_key);
            stripe.redirectToCheckout({
                // Make the id field from the Checkout Session creation API response
                // available to this file, so you can provide it as parameter here
                // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
                sessionId: data.checkout_session_id
            }).then(function (result) {
                // If `redirectToCheckout` fails due to a browser or network
                // error, display the localized error message to your customer
                // using `result.error.message`.
            });
        })
});