import React, { useEffect, useReducer } from "react";
import { Link, withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { makeLengthValidator } from "../../utils/field-validators";
import { submitLogin } from "../../api";
import NO_ERROR from "../../constants/NoError";
import { loginSubmitted } from "../../actions/auth-actions";

import FieldError from "../FieldError/FieldError";
// import './LoginScreen.css'

const textValidators = {
  username: username =>
    makeLengthValidator(8, 17)(username)
      ? NO_ERROR
      : {
          text: "Username must be between 8 and 16 characters long",
          field: "username"
        },
  password: password =>
    makeLengthValidator(1)(password)
      ? NO_ERROR
      : { text: "Password cannot be empty", field: "password" }
};

const LoginScreen = props => {
  const initialState = {
    username: "",
    password: "",
    rememberUsername: false,
    canSubmit: false,
    error: NO_ERROR,
    showError: false
  };

  useEffect(() => {
    // Redirets to game screen
    if (props.showComponents.loadingScreen || props.showComponents.gameScreen) {
      props.history.push("/game");
    }
  });

  // Reducer for form validation actions and field updates
  const reducer = (state, action) => {
    switch (action.type) {
      case "UPDATE_USERNAME":
        return { ...state, username: action.value, showError: true };
      case "UPDATE_PASSWORD":
        return { ...state, password: action.value, showError: true };
      case "TOGGLE_REMEMBER_USERNAME":
        return { ...state, rememberUsername: !state.rememberUsername };
      case "NOW_INVALID":
        return { ...state, error: action.error, canSubmit: false };
      case "NOW_VALID":
        return { ...state, error: NO_ERROR, canSubmit: true };
      default:
        return state;
    }
  };
  const [state, dispatch] = useReducer(reducer, initialState);
  // Updates whenever focus leaves the element
  const createHandleOnBlur = field => e => {
    if (field === "username")
      dispatch({ type: "UPDATE_USERNAME", value: e.target.value });
    else dispatch({ type: "UPDATE_PASSWORD", value: e.target.value });
  };
  // Creates a change handler for the username or password field
  const createHandleOnChange = field => e => {
    // Gets errors in the username/password fields
    const usernameError = textValidators["username"](
      field === "username" ? e.target.value : state.username
    );
    const passwordError = textValidators["password"](
      field === "password" ? e.target.value : state.password
    );

    // Dispatch actions
    if (usernameError === NO_ERROR && passwordError === NO_ERROR)
      dispatch({ type: "NOW_VALID" });
    else if (usernameError !== NO_ERROR)
      dispatch({ type: "NOW_INVALID", error: usernameError });
    else
      dispatch({ type: "NOW_INVALID", error: passwordError, showError: true });
  };

  return (
    <div className="login-screen">
      <div className="login-form-container">
        <div className="field-inputs">
          <div className="username-container">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              name="username"
              onBlur={createHandleOnBlur("username")}
              onChange={createHandleOnChange("username")}
            />
          </div>
          <div className="password-container">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              onBlur={createHandleOnBlur("password")}
              onChange={createHandleOnChange("password")}
            />
          </div>
          {/* <FieldError show={state.showError} error={state.error} /> */}
          <div className="remember-user-container">
            <label htmlFor="remember-username">Remember Username</label>
            <input
              type="checkbox"
              name="remember-username"
              onChange={() => dispatch({ type: "TOGGLE_REMEMBER_USERNAME" })}
              checked={state.rememberUsername}
            />
          </div>
        </div>
        <div className="login-buttons">
          <button
            // disabled={!state.canSubmit}

            onClick={e => props.submitLogin(state.username, state.password)}
          >
            Login
          </button>
          <Link to="/register">
            <button>Create Account</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default withRouter(
  connect(
    state => {
      return { showComponents: state.ui.showComponents };
    },
    dispatch => ({
      submitLogin: (username, password) => {
        dispatch(loginSubmitted(username, password));
      }
    })
  )(LoginScreen)
);
