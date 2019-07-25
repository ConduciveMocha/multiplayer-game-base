import {getInitialLoadInfo,loadImageAsset} from '../api/asset-loading';
import {put, takeEvery,take,call,race} from 'redux-saga/effects';
import * as LoadActions from '../actions/load-actions'
import * as SocketActions from '../actions/socket-actions'
import {LOAD_STARTED,START_INITIAL_LOAD, LOAD_SUCCESS,LOAD_FAILED} from '../constants/action-types/load-types';
import {GameAsset} from '../game/game-object'
import {dispatch} from '../store';
import {flaskServer} from '../constants/urls'

import {ImageAsset} from '../game/game-object';



export function* loadAsset(loadRequest) {
    try {
        loadRequest.gameAsset.initialize(function() {dispatch(LoadActions.loadSuccess(loadRequest.gameAsset))})
        // yield LoadActions.loadStarted(gameObject,loadRequest.assetUrl);
        
    }

    catch(error) {
        console.error(error)
        yield put(LoadActions.loadFailed(loadRequest.gameAsset,error)) 
    }
}


export function* initialLoad() {
    
    const defaultAssetInfo = yield call(getInitialLoadInfo, {});
    
    for(let i  in defaultAssetInfo.assets){
        const asset  = defaultAssetInfo.assets[i]
        if(asset.assetType === 'image') {
            let imgAsset = new ImageAsset(defaultAssetInfo.cdnAddress+asset.url,asset.dim, asset.id)
            yield put(LoadActions.loadStarted(imgAsset))
            loadImageAsset(imgAsset)
        }
    }
    

    for(let i=0; i < defaultAssetInfo.assets.length; i++)
        yield take([LOAD_SUCCESS, LOAD_FAILED]);
    
    yield put(LoadActions.initialLoadFinished())
    yield put(SocketActions.createSocket(flaskServer,'password'))

}


export function* assetLoader() {
    yield take(START_INITIAL_LOAD);
    yield call(initialLoad)

}