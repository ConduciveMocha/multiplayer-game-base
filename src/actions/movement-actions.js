import MovementActionTypes from '../constants/action-types/movement-types';

export const movePlayer = (direction) => {
    return {
        type: MovementActionTypes.MOVE_PLAYER,
        direction: direction
    }
}

export const movePlayerSuccess = (direction) => {
    return {
        type: MovementActionTypes.MOVE_PLAYER_SUCCESS,
        direction:direction
    }
}

export const movePlayerFailed = () => {
    return {
        type: MovementActionTypes.MOVE_PLAYER_FAILED
    }

}