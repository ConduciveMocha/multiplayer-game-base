import { eventChannel } from "redux-saga";
import { take, select, put, call, fork } from "redux-saga/effects";
import io from "socket.io-client";

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

function inventoryChannelSubscrive(socket) {
  return eventChannel(emit => {});
}
