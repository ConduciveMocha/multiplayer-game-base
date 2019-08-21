import React from "react";
import { connect } from "react-redux";
import {
  LOAD_THREADS,
  LOAD_USERS
} from "../../constants/action-types/message-types";

const MagicDebugButton = props => {
  return <button onClick={() => props.sendAll()}>Magic Debug Button!</button>;
};

export default connect(
  state => ({}),
  dispatch => ({
    sendAll: () => {
      dispatch({ type: LOAD_USERS });
      dispatch({ type: LOAD_THREADS, user: 1 });
    }
  })
)(MagicDebugButton);
