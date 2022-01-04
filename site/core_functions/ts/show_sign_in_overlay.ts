/**
 * Shows the sign in/up overlay.
 */
export const show_sign_in_overlay = () => {
  const script = document.createElement("script");
  script.src = "/static/accounts/js/login_overlay.min.js";
  document.body.appendChild(script);
};
