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
import io from "socket.io-client";
import {
  handleMessageIO,
  messageConnect
} from "./socket-sagas/message-socket-saga";
import {
  inventoryIO,
  handleInventoryIO,
  inventoryConnect
} from "./socket-sagas/inventory-socket-saga";

import { handleGameIO, gameConnect } from "./socket-sagas/game-socket-saga";

/**
 * Connect Functions:
 *
 * Error out when I try to make a function that creates these
 * by passing a URL arg
 */
// Returns a socket connection to url
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
    const inventorySocket = yield call(inventoryConnect);

    console.log(
      "SEND_IDENTIFICATION called in socket-sagas.js--Potentially remove this code"
    );
    let idEvent = yield take("SEND_IDENTIFICATION");
    messageSocket.emit("SEND_IDENTIFICATION", {
      user: { id: 1, username: "TestUser" }
    });
    console.log(
      "Finished SEND_IDENTIFICATION in socket-sagas.js -- Potentially remove this code"
    );

    const messageTask = yield fork(handleMessageIO, messageSocket);
    const gameTask = yield fork(handleGameIO, gameSocket);
    const inventoryTask = yield fork(handleInventoryIO, inventorySocket);
    yield take("NOTHING");
  }
}

export default function* socketSaga() {
  yield fork(flow);
}
//
