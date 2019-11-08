import { eventChannel } from "redux-saga";
import { take, takeEvery, select, put, call, fork } from "redux-saga/effects";
import io from "socket.io-client";

import socketLogger from "../socket-logger";

import * as inventoryTypes from "../../constants/action-types/inventory-types";
import * as inventoryActions from "../../actions/inventory-actions";

export function inventoryConnect() {
  const socket = io.connect("http://localhost:5000/inventory", {
    forceNew: true
  });
  return new Promise(resolve => {
    socket.on("connect", () => {
      console.log("Inventory socket connected");
      resolve(socket);
    });
  });
}

function inventoryChannelSubscribe(socket) {
  return eventChannel(emit => {
    socket.on(inventoryTypes.ACQUIRE_ITEM_CONFIRMED, payload => {
      socketLogger.recieved(inventoryTypes.ACQUIRE_ITEM_CONFIRMED, payload);
      emit(inventoryActions.acquireItemConfirmed(payload.itemId));
    });

    socket.on(inventoryTypes.DELETE_ITEM_CONFIRMED, payload => {
      socketLogger.recieved(inventoryTypes.DELETE_ITEM_CONFIRMED, payload);
      emit(inventoryActions.dropItemConfirmed(payload.itemId));
    });

    socket.on(inventoryTypes.DROP_ITEM_CONFIRMED, payload => {
      socketLogger.recieved(inventoryTypes.DROP_ITEM_CONFIRMED, payload);
      emit(inventoryActions.deleteItemConfirmed(payload.itemId));
    });

    socket.on(inventoryTypes.ACQUIRE_ITEM_ERROR, payload => {
      socketLogger.error(inventoryTypes.ACQUIRE_ITEM_ERROR, payload);
      emit(
        inventoryActions.acquireItemError(payload.itemId, payload.errorMessage)
      );
    });

    socket.on(inventoryTypes.DELETE_ITEM_ERROR, payload => {
      socketLogger.error(inventoryTypes.DELETE_ITEM_ERROR, payload);
      emit(
        inventoryActions.deleteItemError(payload.itemId, payload.errorMessage)
      );
    });

    socket.on(inventoryTypes.DROP_ITEM_ERROR, payload => {
      socketLogger.error(inventoryTypes.DROP_ITEM_ERROR, payload);
      emit(
        inventoryActions.dropItemError(payload.itemId, payload.errorMessage)
      );
    });
    return () => {};
  });
}

function* readInventorySocket(socket) {
  const channel = yield call(inventoryChannelSubscribe, socket);
  while (true) {
    let action = yield take(channel);
    yield put(action);
  }
}

function* writeAcquireItem(socket) {
  function sendAcquireItem(action) {
    let payload = { ...action };
    socketLogger.sent(inventoryTypes.ACQUIRE_ITEM, payload);
    socket.emit(inventoryTypes.ACQUIRE_ITEM, payload);
  }

  while (true) {
    let action = yield take(inventoryTypes.ACQUIRE_ITEM);
    console.log("Here");
    sendAcquireItem(action);
  }
}
//! USES DEFAULT VALUE FOR USER ID
function* writeDropItem(socket) {
  function sendDropItem(action) {
    console.log(action);
    let payload = { ...action, userId: 1 };
    socketLogger.sent(inventoryTypes.DROP_ITEM, payload);
    socket.emit(inventoryTypes.DROP_ITEM, payload);
  }

  while (true) {
    console.log("Tkaing a writeDropItem action");
    let action = yield take(inventoryTypes.DROP_ITEM);
    console.log("Here");
    sendDropItem(action);
  }
}

function* writeDeleteItem(socket) {
  function sendDeleteItem(action) {
    let payload = { ...action };
    socketLogger.sent(inventoryTypes.DELETE_ITEM, payload);
    socket.emit(inventoryTypes.DELETE_ITEM, payload);
  }

  while (true) {
    let action = yield take(inventoryTypes.DELETE_ITEM);
    console.log("Here");
    sendDeleteItem(action);
  }
}

function* writeInventorySocket(socket) {
  console.log("writeInventorySocket");

  while (true) {
    console.log(
      "In while statement. If this isnt working. Its this take statement"
    );
    const test = yield take();
    console.log("Test: ", test);
    const action = yield take([
      inventoryTypes.ACQUIRE_ITEM,
      inventoryTypes.DELETE_ITEM,
      inventoryTypes.DROP_ITEM
    ]);
    console.log("Passed the fucky sttatement. It might be socketLoggerthen?");
    socketLogger.sent(action.type, action);
    switch (action.type) {
      case inventoryTypes.ACQUIRE_ITEM:
        socket.emit(inventoryTypes.ACQUIRE_ITEM, action);
      case inventoryTypes.DELETE_ITEM:
        socket.emit(inventoryTypes.DELETE_ITEM, action);
      case inventoryTypes.DROP_ITEM:
        console.log("sendDropItem called on socket: ", socket);
        socket.emit(inventoryTypes.DROP_ITEM, action);
      default:
        console.error("Could not route action type:", action.type);
    }
  }
}

export function* handleInventoryIO(socket) {
  console.log("handleInventoryIO called");
  yield fork(readInventorySocket, socket);
  // yield fork(writeInventorySocket, socket);
  yield fork(writeAcquireItem, socket);
  yield fork(writeDropItem, socket);
  yield fork(writeDeleteItem, socket);
}

export function* inventoryIO() {
  const socket = inventoryConnect();
  yield handleInventoryIO(socket);
}
