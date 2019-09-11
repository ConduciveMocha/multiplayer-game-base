import { eventChannel, END } from "redux-saga";
import {
  take,
  select,
  put,
  call,
  all,
  actionChannel,
  fork,
  cancel
} from "redux-saga/effects";
import * as SocketActions from "../actions/socket-actions";
import * as SocketTypes from "../constants/action-types/socket-types";
import io from "socket.io-client";
import * as MessageActions from "../actions/message-actions";
import * as GameActions from "../actions/game-actions";
import * as MessageTypes from "../constants/action-types/message-types";
import * as GameTypes from "../constants/action-types/game-types";

import { messageConnect, handleMessageIO } from "./message-socket-saga";
import { gameConnect, handleGameIO } from "./game-socket-saga";

export function connect() {
  const socket = io.connect("http://localhost:5000"); // you need to explicitly tell it to use websockets});
  console.log("Connecting to default namespace");
  return new Promise(resolve => {
    socket.on("connect", () => {
      resolve(socket);
    });
  });
}

function* flow() {
  while (true) {
    const messageSocket = yield call(messageConnect);
    const gameSocket = yield call(gameConnect);

    let idEvent = yield take("SEND_IDENTIFICATION");
    console.log("Id event read");
    messageSocket.emit("SEND_IDENTIFICATION", {
      user: { id: 1, username: "TestUser" }
    });

    const mTask = yield fork(handleIO, messageSocket);
    const gTaks = yield fork(handleGameIO, gameSocket);
    console.log("HandleIO Forked");

    yield take("NOTHING");
  }
}
export default function* socketSage() {
  yield fork(flow);
}
