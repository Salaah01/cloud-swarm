import React, { useRef } from "react";
import classes from "./SignUp.module.scss";
import { anyPropsObj } from "../../../../../core_functions/ts/interfaces";
import { check_password_strength } from "../../../../../core_functions/ts";
import {
  get_csrf_token,
  BuildURL,
} from "../../../../../core_functions/ts";

const buildURL = new BuildURL();
// const COMM_PREF_KEYS = (fetch_config("sales") as any).comm_pref_keys;

const sign_up = (props: anyPropsObj) => {
  /**Sends the form when the user attempts to sing up and either updates the
   * error message or reloads the form depending on whether or not the user
   * was able to sign up.
   */

  const formRef = useRef<HTMLFormElement>(null);

  /**Scrolls to the top of the form. */
  const scrollToTop = () => {
    if (formRef.current) {
      formRef.current.scrollIntoView();
    }
  };

  const sign_up_btn_handler = () => {
    // Declaring variables.
    const firstName = document.getElementById(
      "login-overlay-first-name"
    ) as HTMLInputElement;
    const lastName = document.getElementById(
      "login-overlay-last-name"
    ) as HTMLInputElement;
    const email = document.getElementById(
      "login-overlay-email"
    ) as HTMLInputElement;
    const password = document.getElementById(
      "login-overlay-password"
    ) as HTMLInputElement;
    const confirmPassword = document.getElementById(
      "login-overlay-confirm-password"
    ) as HTMLInputElement;
    const termsAccepted = document.getElementById(
      "login-overlay-tc"
    ) as HTMLInputElement;
    const recaptcha = document.getElementById(
      "g-recaptcha-response"
    ) as HTMLInputElement;
    const postActions = document.getElementById(
      "post-actions"
    ) as null | HTMLInputElement;
    const postActionKwargs = document.getElementById(
      "post-action-kwargs"
    ) as null | HTMLInputElement;
    // Check that the terms and conditions have been accepted.
    if (!termsAccepted.checked) {
      props.updateErrorMessage("Please read and accept terms and conditions.");
      scrollToTop();
      return;
    }

    // Check that the passwords match.
    if (password.value !== confirmPassword.value) {
      props.updateErrorMessage("Passwords do not match");
      password.classList.add(classes.input__invalid);
      confirmPassword.classList.add(classes.input__invalid);
      scrollToTop();
      return;
    }

    // Check the password strength.
    const passwordWeaknesses = check_password_strength(password.value);
    if (passwordWeaknesses.length) {
      props.updateErrorMessage(passwordWeaknesses.join("\n"));
      password.classList.add(classes.input__invalid);
      scrollToTop();
      return;
    }

    // Send a post request with sign up details and attempt to login.
    const xhr = new XMLHttpRequest();
    xhr.open("POST", buildURL.sign_up_api(), true);
    xhr.setRequestHeader("X-CSRFToken", get_csrf_token() || "");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    // Clear errors just before sending.
    password.classList.remove(classes.input__invalid);
    confirmPassword.classList.remove(classes.input__invalid);

    xhr.send(
      JSON.stringify({
        firstName: firstName.value,
        lastName: lastName.value,
        email: email.value,
        password: password.value,
        confirmPassword: confirmPassword.value,
        // [COMM_PREF_KEYS.blogs]: (document.getElementById(
        //   "login-overlay-comm-prefs-blogs"
        // ) as HTMLInputElement).checked,
        // [COMM_PREF_KEYS.newsletters]: (document.getElementById(
        //   "login-overlay-comm-prefs-news"
        // ) as HTMLInputElement).checked,
        // [COMM_PREF_KEYS.promotions]: (document.getElementById(
        //   "login-overlay-comm-prefs-promos"
        // ) as HTMLInputElement).checked,
        // [COMM_PREF_KEYS.termsAccepted]: (document.getElementById(
        //   "login-overlay-tc"
        // ) as HTMLInputElement).checked,
        "g-recaptcha-response": recaptcha.value,
        postActions: postActions ? postActions.value.split("|") : [],
        postActionKwargs: postActionKwargs ? postActionKwargs.value : {},
      })
    );


    xhr.onreadystatechange = function () {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        const response = JSON.parse(xhr.responseText);
        if (response.success) {
          location.reload();
        } else {
          props.updateErrorMessage(response.error);
          scrollToTop();
          return;
        }
      }
    };
  };

  const form = () => {
    return (
      <form ref={formRef}>
        <h2 className={`heading-2 ${classes.heading}`}>Sign Up</h2>
        <p className={classes.error_msg}>{props.errorMsg}</p>
        <div className={classes.form_element}>
          <label className={classes.label} htmlFor="login-overlay-first-name">
            First Name
          </label>
          <input
            type="text"
            className={classes.input}
            id="login-overlay-first-name"
            placeholder="First Name"
            required
          />
        </div>
        <div className={classes.form_element}>
          <label className={classes.label} htmlFor="login-overlay-last-name">
            Last Name
          </label>
          <input
            type="text"
            className={classes.input}
            id="login-overlay-last-name"
            placeholder="Last Name"
            required
          />
        </div>
        <div className={classes.form_element}>
          <label htmlFor="login-overlay-email" className={classes.label}>
            Email Address
          </label>
          <input
            className={classes.input}
            id="login-overlay-email"
            type="email"
            name="email"
            placeholder="Email"
            required
          />
        </div>
        <div className={classes.form_element}>
          <label htmlFor="login-overlay-password" className={classes.label}>
            Password
          </label>
          <input
            className={classes.input}
            id="login-overlay-password"
            type="password"
            name="password"
            placeholder="Password"
          />
        </div>
        <div className={classes.form_element}>
          <label
            htmlFor="login-overlay-confirm-password"
            className={classes.label}
          >
            Confirm Password
          </label>
          <input
            className={classes.input}
            id="login-overlay-confirm-password"
            type="password"
            name="confirm-password"
            placeholder="Confirm Password"
          />
        </div>
        <div className={classes.comm_prefs}>
          <div
            className={`${classes.form_element} ${classes.comm_prefs__form_element}`}
          >
            <label
              htmlFor="login-overlay-tc"
              className={`${classes.Label} ${classes.comm_prefs__form_element__label}`}
            >
              I have read and I accept the{" "}
              <a href={buildURL.terms_and_conditions()}>terms and conditions</a>
              .
            </label>
            <input type="checkbox" name="tc" id="login-overlay-tc" />
          </div>
          <div
            className={`${classes.form_element} ${classes.comm_prefs__form_element}`}
          >
            <label
              htmlFor="login-overlay-comm-prefs-promos"
              className={`${classes.Label} ${classes.comm_prefs__form_element__label}`}
            >
              Send me information on new promotions.
            </label>
            <input
              type="checkbox"
              name="pref-blog-promos"
              id="login-overlay-comm-prefs-promos"
            />
          </div>
          <div
            className={`${classes.form_element} ${classes.comm_prefs__form_element}`}
          >
            <label
              htmlFor="login-overlay-comm-prefs-blogs"
              className={`${classes.Label} ${classes.comm_prefs__form_element__label}`}
            >
              Send me information on new blog releases.
            </label>
            <input
              type="checkbox"
              name="pref-blog-blogs"
              id="login-overlay-comm-prefs-blogs"
            />
          </div>
          <div
            className={`${classes.form_element} ${classes.comm_prefs__form_element}`}
          >
            <label
              htmlFor="login-overlay-comm-prefs-news"
              className={`${classes.Label} ${classes.comm_prefs__form_element__label}`}
            >
              Send me newsletters.
            </label>
            <input
              type="checkbox"
              name="pref-blog-news"
              id="login-overlay-comm-prefs-news"
            />
          </div>
        </div>
        <input
          type="hidden"
          id="g-recaptcha-response"
          name="g-recaptcha-response"
        />
        <a href={buildURL.reset_password()}>Forgotten your password?</a>
        <div className={classes.btns}>
          <button
            aria-label="Sign Up"
            className={`btn btn--primary ${classes.btn}`}
            onClick={(event) => {
              event.preventDefault();
              sign_up_btn_handler();
            }}
          >
            Sign Up
          </button>
          <button
            aria-label="Login"
            className={`btn btn--secondary ${classes.btn}`}
            onClick={(event) => {
              event.preventDefault();
              props.updateErrorMessage("");
              props.showLoginPage();
            }}
          >
            Login
          </button>
        </div>
      </form>
    );
  };

  return form();
};

export default sign_up;
