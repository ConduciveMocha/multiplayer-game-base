import LoadActions from '../constants/action-types/load-types';

/** Action created when asset has began loading
 * 
 * @param {string} gameAsset 
 */
export const loadStarted = (gameAsset) => {
    return  {
        type: LoadActions.LOAD_STARTED,
        gameAsset
    }
}

/** Action created when asset has loaded successfully
 * 
 * @param {string} gameAsset 
 */
export const loadSuccess = (gameAsset) => {
    return {
        type: LoadActions.LOAD_SUCCESS,
        gameAsset
    }
}

export const loadFailed = (gameAsset,error) => {
    return {
        type: LoadActions.LOAD_FAILED,
        gameAsset,
        error
    }
}

export const startInitialLoad = () => {
    return{     
        type: LoadActions.START_INITIAL_LOAD
    }
}

export const initialLoadFinished = () => {
    return {
        type:LoadActions.INITIAL_LOAD_FINISHED
    }
}