// import MovementActions, { MOVE_PLAYER } from '../constants/action-types/movement-types'







const initialGameState = {
  gameObjects: {
    0:{},
    1:{},
    2:{},
    3:{},
  }
};
export default function gameReducer(state = initialGameState, action) {
  switch (action.type) {
    default:
      return state;
  }
}
