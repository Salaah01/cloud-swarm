let stripe = Stripe(
  (document.getElementById('stripe-key') as HTMLInputElement).value
);


/**
 * Creates a Stripe card element and renders it into the DOM.
 * @returns {stripe.elements.Element} The Stripe card element.
 */
const card_elem = () => {
  let elements = stripe.elements();
  let style = {
    base: {
      color: '#32325d',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    }
  };

  // Create an instance of the card Element and mount it into the DOM.
  let card = elements.create('card', { style: style });
  console.log('mounting card element');
  card.mount('#card-element');

  // Handle real-time validation errors from the card Element.
  card.on('change', (event) => {
    if (event && event.error) {
      displayError(event);
    }
  })

  return card;
}

/**
 * Displays error messages from the card Element.
 * @param event - The event object.
 * @returns {void}
 */
const displayError = (event: stripe.elements.ElementChangeResponse) => {
  // changeLoadingStatePrices(false);
  let displayError = document.getElementById('card-element-errors') as HTMLDivElement;
  displayError.textContent = event.error!.message || '';
}

const submitBtnHandler = (btn: HTMLButtonElement, card: stripe.elements.Element, callback: Function | null = null) => {
  btn.addEventListener('click', async (event) => {
    event.preventDefault();
    const name = 'Salaah';

    // Create payment method and confirm payment intent.
    stripe.confirmCardPayment(
      (document.querySelector('#client-secret') as HTMLInputElement).value,
      {
        payment_method: {
          card: card,
          billing_details: {
            name: name
          }
        }
      }).then((result) => {
        if (result.error) {
          alert(result.error.message);
        } else {
          if (callback) {
            callback(result);
          }
        }
      })
  })
}

console.log('subscription.ts loaded');
const card = card_elem();

console.log(document.querySelector('#stripe-form-submit'));


submitBtnHandler(
  document.querySelector('#stripe-form-submit') as HTMLButtonElement,
  card,
);

