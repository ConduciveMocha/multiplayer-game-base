import LoadActions from '../constants/action-types/load-types';
import LoadStates from '../constants/LoadStates';
import {dispatch} from '../store'



const initialLoadStates = {
    gameAssets:[],
};

const updateLoadState = (id,  newState, gameAssets, setToNull=false) =>  {
    let newgameAssetList = gameAssets.slice();
    newgameAssetList[id] = {...gameAssets[id], loadState:newState, asset:setToNull ? null : gameAssets[id].asset}
    return newgameAssetList;
}
const checkLoadFinished = (gameAssets) => {
    let result =  gameAssets.every((x) => {
        return (x.loadState === LoadStates.SUCCESSFUL || x.loadState === LoadStates.FAILED)
    });

    return result;
}


export default function loadReducer(state=initialLoadStates, action) {

    switch(action.type){

        case LoadActions.START_INITIAL_LOAD:
            return {...state}
        case LoadActions.INITIAL_LOAD_FINISHED:
            return {...state}

        case LoadActions.LOAD_SUCCESS:{
            const updatedGameAssetList = updateLoadState(action.gameAsset.id, LoadStates.SUCCESSFUL, state.gameAssets);
            
            return {
                gameAssets:updatedGameAssetList
            }
            
        }
        
        case LoadActions.LOAD_FAILED:{
            const updatedGameAssetList = updateLoadState(action.gameAsset.id, LoadStates.FAILED, state.gameAssets, true);
            return {
                gameAssets:updatedGameAssetList
            };
        }

        case LoadActions.LOAD_STARTED:{
            action.gameAsset.setID(state.gameAssets.length);
            return {gameAssets:[...state.gameAssets, action.gameAsset]}
        }
 

        default:{
            return state;
        }
    }
}