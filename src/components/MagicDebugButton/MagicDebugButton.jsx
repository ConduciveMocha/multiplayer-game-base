import React from "react";
import { connect } from "react-redux";
import {
  LOAD_THREADS,
  LOAD_USERS
} from "../../constants/action-types/message-types";

const MagicDebugButton = props => {
  return (
    <>
      <button onClick={() => props.sendIdentification()}>
        SEND IDENTIFICATION!!!!
      </button>
      <button onClick={() => props.sendAll()}>Magic Debug Button!</button>
    </>
  );
};

export default connect(
  state => ({}),
  dispatch => ({
    sendIdentification: () => {
      dispatch({ type: "SEND_IDENTIFICATION", user: 1 });
    },

    sendAll: () => {
      dispatch({ type: LOAD_USERS });
      dispatch({ type: LOAD_THREADS, user: 1 });
    }
  })
)(MagicDebugButton);
