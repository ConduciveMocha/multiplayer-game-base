import MovementActions, { MOVE_PLAYER } from '../constants/action-types/movement-types'
import {INITIAL_LOAD_FINISHED} from '../constants/action-types/load-types';

const initialGameState = {}
export default function gameReducer(state=initialGameState, action) {
    switch(action.type) {
        default:
            return state;
    }
}  