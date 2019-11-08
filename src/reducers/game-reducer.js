// import MovementActions, { MOVE_PLAYER } from '../constants/action-types/movement-types'

import * as GameTypes from "../constants/action-types/game-types";
import { inventoryMock, gameObjectsMock } from "../utils/game-mock";
const initialGameState = {
  gameObjects: gameObjectsMock,
  inventory: inventoryMock
};

const updateGameObjects = (oldState, updatedObjects) => {
  let stateCopy = { ...oldState };
  for (let i in updatedObjects) {
    let obj = updatedObjects[i];
    stateCopy[obj.id] = obj;
  }
  return { ...stateCopy };
};

export default function gameReducer(state = initialGameState, action) {
  switch (action.type) {
    case "TEST_CANVAS":
      return {
        ...state,
        gameObjects: {
          ...state.gameObjects,
          49: {
            type: 1,
            x: Math.floor(Math.random() * window.innerWidth * 0.65),
            y: Math.floor(Math.random() * window.innerHeight * 0.5)
          }
        }
      };

    case GameTypes.UPDATE_GAMESTATE:
      console.log("UPDATING GAMESTATE", action);
      return {
        ...state,
        gameObjects: updateGameObjects(state.gameObjects, action.updatedObjects)
      };

    default:
      return state;
  }
}
