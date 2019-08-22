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

export function messageConnect() {
  const socket = io("http://localhost:5000/message", { forceNew: true });
  console.log("Connecting to messaging namespace");
  return new Promise(resolve => {
    socket.on("connect", () => {
      console.log("Message Socket Connected");
      resolve(socket);
    });
  });
}

export function gameConnect() {
  const socket = io("http://localhost:5000/game", { forceNew: true });
  console.log("Connecting to game namespace");
  return new Promise(resolve => {
    socket.on("connect", () => {
      console.log("Game socket connected");
      resolve(socket);
    });
  });
}

function subscribe(socket) {
  return eventChannel(emit => {
    socket.on("test", data => {
      console.log("Test Recieved");
      console.log("Data:", data);
    });

    socket.on(MessageTypes.SERVER_THREAD_REQUEST, payload => {
      console.debug("Request to join thread: ", payload);
      emit(MessageActions.serverThreadRequest(payload));
    });

    socket.on(MessageTypes.NEW_MESSAGE, message => {
      console.log(message);
      emit(MessageActions.recieveMessage(message));
    });

    return () => {};
  });
}

function moveChannelSubscribe(socket) {
  return eventChannel(emit => {
    socket.on(GameTypes.UPDATE_GAMESTATE, payload => {
      console.debug("Updating gamestate with payload:", payload);
      emit(GameActions.updateGamestate(payload.updatedObjects));
    });

    socket.on("TEST", payload => {
      console.log("Movement socket test recieved with payload: ", payload);
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

function* writeRequestThreadJoin(socket){
  function sendRequestThreadJoin(action){
    socket.emit(MessageTypes.CLIENT_THREAD_REQUEST, {...action,sender:0})
    console.log('Sent request to join thread: ', {...action, sender:0})
  }

  while(true){
    let action = yield take(MessageTypes.CLIENT_THREAD_REQUEST)
    sendRequestThreadJoin(action)
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

//! USES DEBUG VALUE FOR PLAYER
function* writeMove(socket) {
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

//! USES DEBUG VALUE FOR PLAYER
const getPlayerObject = state => state.game.gameObjects[0];

//! USES DEBUG VALUE FOR PLAYER
function* writeInventoryAction(socket) {
  function sendRemoveItem(action) {
    console.log("Sending REMOVE_ITEM", action);
    socket.emit(GameTypes.REMOVE_INVENTORY_ITEM, {
      sender: 0,
      item: action.item,
      destination: action.destination
    });
  }

  while (true) {
    let action = yield take(GameTypes.REMOVE_INVENTORY_ITEM);

    console.log("Recieved REMOVE_INVENTORY_ITEM");
    sendRemoveItem(action);
  }
}

function* readMove(socket) {
  const moveChannel = yield call(moveChannelSubscribe, socket);
  while (true) {
    let action = yield take(moveChannel);
    yield put(action);
  }
}

function* handleGameIO(socket) {
  yield fork(readMove, socket);
  yield fork(writeMove, socket);
  yield fork(writeInventoryAction, socket);
}
function* handleIO(socket) {
  yield fork(read, socket);
  yield fork(write, socket);
  yield fork(writeRequestThreadJoin,socket)
}

function* flow() {
  while (true) {
    // const socket = yield call(connect);
    const messageSocket = yield call(messageConnect);
    const gameSocket = yield call(gameConnect);
    // const task = yield fork(handleIO, socket);
    const mTask = yield fork(handleIO, messageSocket);
    const gTaks = yield fork(handleGameIO, gameSocket);
    console.log("HandleIO Forked");
    // socket.emit("SOCKET_TEST", { data: "test" });

    yield take("NOTHIng");
  }
}

export default function* socketSaga() {
  yield fork(flow);
}
//
