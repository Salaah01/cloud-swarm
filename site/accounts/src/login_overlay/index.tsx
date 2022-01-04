import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, compose, combineReducers } from "redux";
import App from "./App";
import overlayControlsReducer from "./store/reducers/overlay_controls";

declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION_COMPOSE__?: typeof compose;
    __REDUX_DEVTOOLS_EXTENSION__?: typeof compose;
  }
}
const composeEnhancer =
  process.env.NODE_ENV === "development"
    ? window.__REDUX_DEVTOOLS_EXTENSION__ &&
      window.__REDUX_DEVTOOLS_EXTENSION__()
    : null || compose;

const rootReducer = combineReducers({
  overlayControls: overlayControlsReducer,
});

const store = createStore(rootReducer, composeEnhancer);

const app = (
  <Provider store={store}>
    <App />
  </Provider>
);

ReactDOM.render(app, document.getElementById('login-overlay'));
