import React from "react";
import classes from "./Login.module.scss";
import { anyPropsObj } from "../../../../../core_functions/ts/interfaces";
import { get_csrf_token, BuildURL } from "../../../../../core_functions/ts";

const buildURL = new BuildURL();

const login = (props: anyPropsObj) => {
  /**Sends the form when the user attempts to login and either updates the
   * error message or reloads the form depending on whether or not the user
   * was able to login.
   */
  const login_btn_handler = () => {
    // Declaring variables.
    const emailInput = document.getElementById(
      "login-overlay-email"
    ) as HTMLInputElement;
    const passwordInput = document.getElementById(
      "login-overlay-password"
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

    // Remove any red borders.
    emailInput.classList.remove(classes.input__invalid);
    passwordInput.classList.remove(classes.input__invalid);
    let error = false;

    // Validate email
    if (
      emailInput.value.search(
        /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/
      ) < 0
    ) {
      emailInput.classList.add(classes.input__invalid);
      error = true;
    }

    // Validate password
    if (!passwordInput.value) {
      passwordInput.classList.add(classes.input__invalid);
      error = true;
    }

    if (error) {
      return;
    }

    // Send a post request with login details and attempt to login.
    const xhr = new XMLHttpRequest();
    xhr.open("POST", buildURL.login_api(), true);
    xhr.setRequestHeader("X-CSRFToken", get_csrf_token() || "");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.send(
      JSON.stringify({
        email: emailInput.value,
        password: passwordInput.value,
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
          return;
        }
      }
    };
  };

  const form = () => {
    return (
      <form>
        <h2 className={`heading-2 ${classes.heading}`}>Login</h2>
        <p className={classes.error_msg}>{props.errorMsg}</p>
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
        <input
          type="hidden"
          id="g-recaptcha-response"
          name="g-recaptcha-response"
        />
        <a href={buildURL.reset_password()}>Forgotten your password?</a>
        <div className={classes.btns}>
          <button
            aria-label="Login"
            className={`btn btn--primary ${classes.btn}`}
            onClick={(event) => {
              event.preventDefault();
              login_btn_handler();
            }}
          >
            Login
          </button>
          <button
            aria-label="Register"
            className={`btn btn--secondary ${classes.btn}`}
            onClick={(event) => {
              event.preventDefault();
              props.updateErrorMessage("");
              props.showSignUpPage();
            }}
          >
            Register
          </button>
        </div>
      </form>
    );
  };

  return form();
};

export default login;
