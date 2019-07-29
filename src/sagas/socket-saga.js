import { eventChannel, END } from "redux-saga";
import {
  take,
  takeEvery,
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
import testAction from "../actions/debug-actions";
import * as MessageTypes from "../constants/action-types/message-types";
import { appendJwt } from "../api";

// Returns a socket connection to url
export function connect() {
  const socket = io.connect("http://localhost:5000"); // you need to explicitly tell it to use websockets});
  return new Promise(resolve => {
    socket.on("connect", () => {
      resolve(socket);
    });
  });
}

export function messageConnect() {
  const socket = io("http://localhost:5000/message", { forceNew: true });
  return new Promise(resolve => {
    socket.on("connect", () => {
      resolve(socket);
    });
  });
}
// export function connect(url,opts) {
//   const socket = io(url,opts);
//   return new Promise(resolve => {
//     socket.on("connect", () => {
//       //socket.emit("TEST",{'shouldnotappear':1, 'url':url});
//       resolve(socket);
//     });
//   });
// }
function subscribe(socket) {
  return eventChannel(emit => {
    socket.on("test", data => {
      console.log("Test Recieved");
      console.log("Data:", data);
    });

    socket.on(MessageTypes.JOIN_THREAD_REQUESTED, payload => {
      console.debug("Request to join thread: ", payload);
      emit(MessageActions.joinThreadRequest(payload));
    });

    socket.on(MessageTypes.NEW_MESSAGE, message => {
      console.log(message);
      emit(MessageActions.recieveMessage(message));
    });

    return () => {};
  });
}

// Generator that takes all actions
function* read(socket) {
  const channel = yield call(subscribe, socket);
  while (true) {
    let action = yield take(channel);
    yield put(action);
  }
}

function* write(socket) {
  function sendMessage(action) {
    socket.emit(MessageTypes.SEND_MESSAGE, { ...action, sender: 0 });
    console.log("Emitted event through socket in sendMessage");
    console.log("action object", action);
    // yield put({type:"MESSAGE_SENT",message:action.message})
  }

  while (true) {
    let action = yield take(MessageTypes.SEND_MESSAGE);
    sendMessage(action);
  }
}

function* handleIO(socket) {
  yield fork(read, socket);
  yield fork(write, socket);
}

function* flow() {
  while (true) {
    const socket = yield call(connect);
    const messageSocket = yield call(messageConnect);
    const task = yield fork(handleIO, socket);
    const mTask = yield fork(handleIO, messageSocket);
    console.log("HandleIO Forked");
    socket.emit("SOCKET_TEST", { data: "test" });

    yield take("NOTHIng");
  }
}

export default function* socketSaga() {
  yield fork(flow);
}
//
