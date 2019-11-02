import { eventChannel } from "redux-saga";
import { take, select, put, call, fork } from "redux-saga/effects";
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

function* writeInventorySocket(socket) {
  function sendAcquireItem(action) {}

  function sendDeleteItem(action) {}

  function sendDropItem(action) {}

  while (true) {
    let action = yield take([
      inventoryTypes.ACQUIRE_ITEM,
      inventoryTypes.DELETE_ITEM,
      inventoryTypes.DROP_ITEM
    ]);

    switch (action.type) {
      case inventoryTypes.ACQUIRE_ITEM:
        sendAcquireItem(action);
      case inventoryTypes.DELETE_ITEM:
        sendDeleteItem(action);
      case inventoryTypes.DROP_ITEM:
        sendDropItem(inventoryTypes.DROP_ITEM);
      default:
        console.error("Could not route action type:", action.type);
    }
  }
}

export function* handleInventoryIO(socket) {
  yield fork(readInventorySocket, socket);
  yield fork(writeInventorySocket, socket);
}

export function* inventoryIO() {
  const socket = inventoryConnect();
  yield handleInventoryIO(socket);
}
