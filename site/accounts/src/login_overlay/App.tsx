import React, { Component } from "react";
import { connect } from "react-redux";
import * as actions from "./store/actions/index";
import { ConnectState } from "../../../core_functions/ts/interfaces";
import * as CONSTANTS from "./constants";
import classes from "./App.module.scss";
import { load_recaptcha } from "../../../core_functions/ts";
import LoginForm from "./components/Login/Login";
import SignUpPage from "./components/SignUp/SignUp";

class App extends Component<any> {
  componentDidMount = () => {
    load_recaptcha(`${this.props.currentPage}_API`);
    this.escBtnHandler();
  };

  componentDidUpdate = () => {
    load_recaptcha(`${this.props.currentPage}_API`);
  };

  /**On pressing the escape key hide the overlay. */
  escBtnHandler = () => {
    window.addEventListener("keydown", (event) => {
      if (this.props.overlayVisible && event.key === "Escape") {
        this.props.onHideOverlay();
      }
    });
  };

  /**Main form element. */
  form = () => {
    if (this.props.currentPage === CONSTANTS.PAGES.login) {
      return (
        <LoginForm
          errorMsg={this.props.errorMsg}
          showSignUpPage={this.props.onShowSignUpPage}
          updateErrorMessage={this.props.onUpdateErrorMessage}
        />
      );
    } else {
      return (
        <SignUpPage
          errorMsg={this.props.errorMsg}
          showLoginPage={this.props.onShowLoginPage}
          updateErrorMessage={this.props.onUpdateErrorMessage}
        />
      );
    }
  };

  render() {
    if (this.props.overlayVisible) {
      return (
        <div
          className={classes.outer_container}
          onMouseDown={this.props.onHideOverlay}
        >
          <div
            className={classes.inner_container}
            onMouseDown={(event: any) => event.stopPropagation()}
          >
            <this.form />
          </div>
        </div>
      );
    } else {
      return <div></div>;
    }
  }
}

const mapStateToProps = (state: ConnectState) => {
  return {
    overlayVisible: state.overlayControls.overlayVisible,
    currentPage: state.overlayControls.currentPage,
    errorMsg: state.overlayControls.errorMsg,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    onHideOverlay: () => dispatch(actions.hideOverlay()),
    onShowSignUpPage: () => dispatch(actions.showSignUpPage()),
    onShowLoginPage: () => dispatch(actions.showLoginPage()),
    onUpdateErrorMessage: (msg: string) =>
      dispatch(actions.updateErrorMessage(msg)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
