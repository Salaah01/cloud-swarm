/**Gets the csrf_token if it exists. */
export const get_csrf_token = () => {
  for (const cookie of document.cookie.split("; ")) {
    if (cookie.startsWith("csrftoken")) {
      return cookie.split("=")[1];
    }
  }
  return;
};
