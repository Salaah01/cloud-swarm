import * as config from "../../cloud_swarm/config.json";

/**
 * Loads the Google recapture script and the function that needs to be run
 * once the script has loaded.
 * @param {String} recaptcha_action - Recapture action.
 */
export const load_recaptcha = (recaptcha_action: string) => {
  const script = document.createElement("script");
  script.src = `https://www.google.com/recaptcha/api.js?render=${config.recaptcha_site_key}`;
  document.body.appendChild(script);
  script.onload = () => {
    const script = document.createElement("script");
    script.innerHTML = `grecaptcha.ready(function () {grecaptcha
          .execute('${config.recaptcha_site_key}', { action: '${recaptcha_action}' })
          .then(function (token) {
            document.getElementById("g-recaptcha-response").value = token;
          });
      });`;
    document.body.append(script);
  };
};
