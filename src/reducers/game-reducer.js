// import MovementActions, { MOVE_PLAYER } from '../constants/action-types/movement-types'

const initialGameState = {
  gameObjects: []
};
export default function gameReducer(state = initialGameState, action) {
  switch (action.type) {
    case "TEST_CANVAS":
      return {
        ...state,
        gameObjects: [
          ...state.gameObjects,
          {
            x: Math.floor(Math.random() * window.innerWidth * 0.65),
            y: Math.floor(Math.random() * window.innerHeight * 0.5)
          }
        ]
      };

    default:
      return state;
  }
}
