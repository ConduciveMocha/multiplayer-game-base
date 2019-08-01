import * as GameTypes from '../constants/action-types/game-types';

export const playerKeyed = (key) =>({
    type: GameTypes.PLAYER_KEYED,
    key
})


export const updateGamestate = (updatedObjects) => ({
    type: GameTypes.UPDATE_GAMESTATE,
    updatedObjects:updatedObjects
})