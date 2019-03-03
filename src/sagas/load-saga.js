import {put, takeEvery,take} from 'redux-saga/effects';
import * as LoadActions from '../actions/load-actions'
import {LOAD_STARTED,START_INITIAL_LOAD, LOAD_SUCCESS} from '../constants/action-types/load-types';
import {GameAsset} from '../game/game-object'
import {dispatch} from '../store';





export function* loadAsset(loadRequest) {
    try {
        loadRequest.gameAsset.initialize(function() {dispatch(LoadActions.loadSuccess(loadRequest.gameAsset))})
        console.log(loadRequest.gameAsset)
        // yield LoadActions.loadStarted(gameObject,loadRequest.assetUrl);
        
    }

    catch(error) {
        console.log('errro')
        yield put(LoadActions.loadFailed(loadRequest.gameAsset,error)) 
    }
}


export function* iniitialLoad() {
    const initAction = yield take(START_INITIAL_LOAD);
    for(let assetUrl in initAction.assetUrls) {
        // TODO
        // create asset here
        let asset=  new  GameAsset(assetUrl); // TEMPORARY CODE
        // end
        
        dispatch(LoadActions.loadStarted(asset))
    } 

    for(let i=0; i < initAction.assetUrls.length; i++) 
        yield take(LOAD_SUCCESS);
    
    

    yield put(LoadActions.initialLoadFinished())
    

}


export function* assetLoader() {
    yield takeEvery(LOAD_STARTED, loadAsset);   
}