/**
 * Builds a URL based on the top level domain and any string that needs to be
 * attached to the end of the domain.
 * @param {String} strToAppend - String to append to the end of the url.
 */
class BuildURL {
  /**
   * Returns the root domain with a string appended at the end of the URL.
   * @param {String} strToAppend - string to append.
   * @returns {String} - URL with string appended.
   */
  append = (strToAppend = "") => {
    return `${location.origin}/${strToAppend}`;
  };

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

export default BuildURL;