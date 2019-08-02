import * as GameTypes from '../constants/action-types/game-types';

export const playerKeyed = (key) =>{
    console.log('Creating ', GameTypes.PLAYER_KEYED)
    return {
    type: GameTypes.PLAYER_KEYED,
    key:key
}}


export const updateGamestate = (updatedObjects) => ({
    type: GameTypes.UPDATE_GAMESTATE,
    updatedObjects:updatedObjects
})