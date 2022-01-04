import { updateObject } from "../../../../../core_functions/ts";
import {
  anyPropsObj,
  reducerAction,
} from "../../../../../core_functions/ts/interfaces";
import * as actionTypes from "../actions/actionTypes";
import * as constants from "../../constants";

export const initialState: anyPropsObj = {
  overlayVisible: true,
  currentPage: constants.PAGES.login,
  errorMsg: "",
};

/**Shows the sign up overlay. */
const showOverlay = (state: anyPropsObj) => {
  return updateObject(state, { overlayVisible: true });
};

/**Hides the sign up overlay. */
const hideOverlay = (state: anyPropsObj) => {
  return updateObject(state, { overlayVisible: false });
};

/**Shows the sign up page. */
const showSignUpPage = (state: anyPropsObj) => {
  return updateObject(state, { currentPage: constants.PAGES.signUp });
};

/**Shows the login page. */
const showLoginPage = (state: anyPropsObj) => {
  return updateObject(state, { currentPage: constants.PAGES.login });
};

/**
 * Updates the error message.
 * @param {String} action.msg - Error message.
 */
const updateErrorMessage = (state: anyPropsObj, action: reducerAction) => {
  return updateObject(state, { errorMsg: action.msg });
};

const reducer = (state = initialState, action: reducerAction) => {
  switch (action.type) {
    case actionTypes.SHOW_OVERLAY:
      return showOverlay(state);
    case actionTypes.HIDE_OVERLAY:
      return hideOverlay(state);
    case actionTypes.SHOW_SIGN_UP_PAGE:
      return showSignUpPage(state);
    case actionTypes.SHOW_LOGIN_PAGE:
      return showLoginPage(state);
    case actionTypes.UPDATE_ERROR_MESSAGE:
      return updateErrorMessage(state, action);
    default:
      return state;
  }
};

export default reducer;
