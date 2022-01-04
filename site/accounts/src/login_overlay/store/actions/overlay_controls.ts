/**Redux Actions */

import * as actionTypes from "./actionTypes";

/**Dispatches action to show the login overlay. */
export const showOverlay = () => {
  return {
    type: actionTypes.SHOW_OVERLAY,
  };
};
/**Dispatches action to hide the login overlay. */
export const hideOverlay = () => {
  return {
    type: actionTypes.HIDE_OVERLAY,
  };
};

/**Dispatches action to show the sign up page. */
export const showSignUpPage = () => {
  return {
    type: actionTypes.SHOW_SIGN_UP_PAGE,
  };
};

/**Dispatches action to show the login page. */
export const showLoginPage = () => {
  return {
    type: actionTypes.SHOW_LOGIN_PAGE,
  };
};

/**Dispatches action to update the error message.
 * @param {String} msg - Error message.
 */
export const updateErrorMessage = (msg: string) => {
  return {
    type: actionTypes.UPDATE_ERROR_MESSAGE,
    msg: msg,
  };
};
