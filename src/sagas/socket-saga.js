import { eventChannel, END } from "redux-saga";
import {
  take,
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
  const socket = io.connect('http://localhost:5000')// you need to explicitly tell it to use websockets});
  return new Promise(resolve => {
    socket.on("connect", () => {
      //socket.emit("TEST",{'shouldnotappear':1, 'url':url});
      resolve(socket);
    });
  });
}

export function messageConnect() {
  const socket = io('http://localhost:5000/message');
  return new Promise(resolve => {
    socket.on("connect", () => {
      //socket.emit("TEST",{'shouldnotappear':1, 'url':url});
      resolve(socket);
    });
  });
}
// export function connect(url) {
//   const socket = io(url);
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
      console.log(data);
      console.log("MESSAGE_SENT");
      // socket.emit("SEND_MESSAGE", "test");

      emit(data);
    });
    socket.on("SOCKET_TEST_2", data => {
      console.log('Emitting SOCKET_TEST2')
      emit("SOCKET_TEST_2");
      emit(data);
    });

    
    //? What is this for? Source: https://github.com/kuy/redux-saga-chat-example/blob/master/src/client/sagas.js
    return () => {

    };
  });
}

// Generator that takes all actions
function* read(socket) {
  const channel = yield call(subscribe, socket);
  while (true) {
    let action = yield take(channel);
    console.log("read:", action);
    // yield put(testAction(action));
  }
}

function* write(socket) {
  while (true) {
    //? Modified this, might be wrong
    const { payload } = yield take(MessageTypes.SEND_MESSAGE);
    socket.emit("message", payload);
  }
}

function* handleIO(socket) {
  yield fork(read, socket);
  yield fork(write, socket);
}

function* flow() {
  // const task = yield fork(handleIO, socket);
  while (true){
    // const messageSocket = yield call(messageConnect);
    const socket = yield call(connect);
    console.log('here')
    console.log('Here')
    console.log('HERE')
    const task = yield fork(handleIO, socket)
    setTimeout(1000)
    socket.emit("SOCKET_TEST",{data:'test'})
    // const mTask = yield fork(handleIO, messageSocket);
    
    console.log('HERE ')
    // messageSocket.emit('NAMESPACE_TEST', {'data':'data'})
    yield take ("NOTHIng")
    // messageSocket.emit('NAMESPACE_TEST', {'data':'data'})
    // socket.emit('SOCKET_TEST')
    // messageSocket.emit("TEST", {'test':2});
    
  }

}


export default function* socketSaga() {
  yield fork(flow);
}
//
