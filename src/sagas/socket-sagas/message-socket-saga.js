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
import * as SocketActions from "../../actions/socket-actions";
import * as SocketTypes from "../../constants/action-types/socket-types";
import io from "socket.io-client";
import * as MessageActions from "../../actions/message-actions";
import * as GameActions from "../../actions/game-actions";
import * as MessageTypes from "../../constants/action-types/message-types";
import * as GameTypes from "../../constants/action-types/game-types";
import { getPlayerObject } from "./game-socket-saga";
export function messageConnect() {
  const socket = io.connect("http://localhost:5000/message", {
    forceNew: true
  });
  console.log("Connecting to messaging namespace");
  return new Promise(resolve => {
    socket.on("connect", () => {
      console.log("Message Socket Connected");
      resolve(socket);
    });
  });
}

function messageChannelSubscribe(socket) {
  return eventChannel(emit => {
    socket.on("test", data => {
      console.log("Test Recieved");
      console.log("Data:", data);
    });

    socket.on("join", data => {
      socket.emit("join", data);
    });

    socket.on("REQUEST_NEW_THREAD", payload => {
      console.debug("Request to join thread: ", payload);
      socket.join(`thread-${payload.thread}`);
      console.log("REQUEST_NEW_THREAD succesful. Calling serverThreadRequest");
      emit(MessageActions.serverThreadRequest(payload));
    });

    socket.on("NEW_THREAD_CREATED", payload => {
      console.log("New thread created:", payload);
      // socket.join(`thread-${payload.thread}`);
      emit(MessageActions.serverThreadRequest(payload));
      console.log("SENDING MESSAGE: ", payload);
      emit(MessageActions.sendMessage(payload.id, payload.content));
    });

    socket.on("NEW_MESSAGE", message => {
      console.log("NEW_MESSAGE: ", message);
      emit(MessageActions.recieveMessage(message));
    });
    // TODO FIX
    //! USES DEBUG VALUE FOR USER ID. DOES NOT ACTUALLY READ VALUE
    socket.on("SEND_IDENTIFICATION", payload => {
      console.log("Sending user identification");
      socket.emit("USER_IDENTIFICATION", {
        user: { id: 1, username: "testUSER" }
      });
    });

    return () => {};
  });
}

// Generator that takes all actions
// Reads message event FROM backend
function* readMessageChannel(socket) {
  const channel = yield call(messageChannelSubscribe, socket);
  while (true) {
    let action = yield take(channel);
    console.log("Read event from message channel: ", action);
    yield put(action);
  }
}
// Writes thread event TO backend
function* writeRequestThreadJoin(socket) {
  function sendRequestThreadJoin(action) {
    socket.emit(MessageTypes.REQUEST_NEW_THREAD, { ...action, sender: 1 });
    console.log("Sent request to join thread: ", { ...action, sender: 1 });
  }

  while (true) {
    let action = yield take(MessageTypes.REQUEST_NEW_THREAD);
    sendRequestThreadJoin(action);
  }
}

// Writes message event TO backend
function* writeMessageEvent(socket) {
  function sendMessage(action) {
    socket.emit(MessageTypes.SEND_MESSAGE, { ...action, sender: 1 });
    console.log("Emitted event through socket in sendMessage");
    console.log("action object", action);
    // yield put({type:"MESSAGE_SENT",message:action.message})
  }

  while (true) {
    let action = yield take(MessageTypes.SEND_MESSAGE);
    sendMessage(action);
  }
}

//! USES DEBUG VALUE FOR PLAYER
function* writeMoveEvent(socket) {
  function sendMove(action) {
    console.log("Sending move", action.key);
    socket.emit(GameTypes.PLAYER_KEYED, {
      sender: 0,
      key: action.key,
      playerObject: action.playerObject
    });
  }
  while (true) {
    let action = yield take(GameTypes.PLAYER_KEYED);
    let playerObject = yield select(getPlayerObject);
    console.log("Player Object before send: ", playerObject);
    console.log("Recieved PLAYER_KEYED");
    sendMove({ ...action, playerObject: playerObject });
  }
}

export function* handleMessageIO(socket) {
  yield fork(readMessageChannel, socket);
  yield fork(writeMessageEvent, socket);
  yield fork(writeRequestThreadJoin, socket);
}

export function* messageIO() {
  const socket = messageConnect();
  yield handleMessageIO(socket);
}
