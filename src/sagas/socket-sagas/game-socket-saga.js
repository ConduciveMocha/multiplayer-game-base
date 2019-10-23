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

import * as SocketActions from "../../actions/socket-actions";
import * as SocketTypes from "../../constants/action-types/socket-types";
import * as MessageActions from "../../actions/message-actions";
import * as GameActions from "../../actions/game-actions";
import * as MessageTypes from "../../constants/action-types/message-types";
import * as GameTypes from "../../constants/action-types/game-types";

//! USES DEBUG VALUE FOR PLAYER
export const getPlayerObject = state => state.game.gameObjects[0];

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

//! USES DEBUG VALUE FOR PLAYER
function* writeInventoryEvent(socket) {
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

export function* handleGameIO(socket) {
  yield fork(readMove, socket);
  yield fork(writeMoveEvent, socket);
  yield fork(writeInventoryEvent, socket);
}
