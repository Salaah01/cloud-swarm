/**Unit tests for the `overlay_controls` reducer. */

import OverlayControls from "./overlay_controls";
import * as actionTypes from "../actions/actionTypes";
import * as CONSTANTS from "../../constants";

describe("SHOW_OVERLAY", () => {
  const state = {
    overlayVisible: false,
    a: 1,
  };

  const reducer = OverlayControls(state, {
    type: actionTypes.SHOW_OVERLAY,
  });

  it("should set the overlay to visible.", () => {
    expect(reducer).toEqual({
      overlayVisible: true,
      a: 1,
    });
  });

  it("should not mutate the original state.", () => {
    expect(state).toEqual({
      overlayVisible: false,
      a: 1,
    });
  });
});

describe("HIDE OVERLAY", () => {
  const state = {
    overlayVisible: true,
    a: 1,
  };

  const reducer = OverlayControls(state, {
    type: actionTypes.HIDE_OVERLAY,
  });

  it("should set the overlay to not visible.", () => {
    expect(reducer).toEqual({
      overlayVisible: false,
      a: 1,
    });
  });

  it("should not mutate the original state.", () => {
    expect(state).toEqual({
      overlayVisible: true,
      a: 1,
    });
  });
});

describe("SHOW_SIGN_UP_PAGE", () => {
  const state = {
    currentPage: CONSTANTS.PAGES.login,
    a: 1,
  };

  const reducer = OverlayControls(state, {
    type: actionTypes.SHOW_SIGN_UP_PAGE,
  });

  it("should show the sign up page.", () => {
    expect(reducer).toEqual({
      currentPage: CONSTANTS.PAGES.signUp,
      a: 1,
    });
  });

  it("should not mutate the original state.", () => {
    expect(state).toEqual({
      currentPage: CONSTANTS.PAGES.login,
      a: 1,
    });
  });
});

describe("SHOW_LOGIN_PAGE", () => {
  const state = {
    currentPage: CONSTANTS.PAGES.signUp,
    a: 1,
  };

  const reducer = OverlayControls(state, {
    type: actionTypes.SHOW_LOGIN_PAGE,
  });

  it("should show the login page.", () => {
    expect(reducer).toEqual({
      currentPage: CONSTANTS.PAGES.login,
      a: 1,
    });
  });

  it("should not mutate the original state.", () => {
    expect(state).toEqual({
      currentPage: CONSTANTS.PAGES.signUp,
      a: 1,
    });
  });
});

describe("UPDATE_ERROR_MESSAGE", () => {
  const state = {
    errorMsg: "abc",
    a: 1,
  };

  const reducer = OverlayControls(state, {
    type: actionTypes.UPDATE_ERROR_MESSAGE,
    msg: "def",
  });

  it("should update the error message.", () => {
    expect(reducer).toEqual({
      errorMsg: "def",
      a: 1,
    });
  });

  it("should not mutate the original state.", () => {
    expect(state).toEqual({
      errorMsg: "abc",
      a: 1,
    });
  });
});
