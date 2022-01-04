/**
 * Builds a URL based on the top level domain and any string that needs to be
 * attached to the end of the domain.
 * @param {String} strToAppend - String to append to the end of the url.
 */
export class BuildURL {
  /**
   * Returns the root domain with a string appended at the end of the URL.
   * @param {String} strToAppend - string to append.
   */
  append = (strToAppend = "") => {
    return `${location.origin}/${strToAppend}`;
  };

  /**Returns the terms and conditions page. */
  terms_and_conditions = () => {
    return this.append("terms-and-conditions");
  };



  // /**Returns the URL to the basket page. */
  // basket_page = () => {
  //   return this.append("sales/basket");
  // };

  // /**Returns the URL to the checkout page. */
  // checkout_page = () => {
  //   return this.append("sales/checkout/");
  // };

  // /**Checkout confirmation page. */
  // checkout_confirmation_page = () => {
  //   return this.append("sales/checkout-confirmation/");
  // };

  // /**Returns the URL to the transactions API. */
  // transactions_api = () => {
  //   return this.append("sales/transactions-api");
  // };

  // /**Returns the URL ot the transaction page.
  //  * @param {Number} transactionID - transaction ID.
  //  */
  // invoice_page = (transactionID: number) => {
  //   return this.append(`sales/invoice/${transactionID}`);
  // };

  // /**Returns the URL for the basket API. */
  // basket_api = () => {
  //   return this.append("sales/basket-api/");
  // };

  /**Returns the login API URL. */
  login_api = () => {
    return this.append("accounts/login-api/");
  };

  /**Returns the sign up API URL. */
  sign_up_api = () => {
    return this.append("accounts/sign-up-api/");
  };

  /**Returns the password reset URL. */
  reset_password = () => {
    return this.append("accounts/reset-password/");
  };

  // /**Returns the URL to update the user's communication preferences. */
  // update_comm_prefs_api = () => {
  //   return this.append("accounts/update-comm-prefs-api/");
  // };

  /**
   * Site verification check API endpoint.
   * @param id - Site ID. 
   * @param slug - Site slug. 
   * @returns {String} - URL to the site verification check API endpoint.
   */
  siteVerificationCheckAPI = (id: number, slug: string) => {
    return this.append(`sites/${id}-${slug}/verification-check/`);
  }

}
