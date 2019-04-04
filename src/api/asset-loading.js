import {flaskServer,staticServer} from './urls';
import LoadStates from '../constants/LoadStates'
import {loadSuccess,loadFailed} from '../actions/load-actions'
import {dispatch} from '../store'
export async function getInitialLoadInfo(payload) {
    const url = flaskServer + '/initial-load-info'
    const response = await fetch(url)
    return await response.json()
}

export function loadImageAsset(imgAsset) {
    const url = imgAsset.assetUrl;
    imgAsset.asset = new Image();
    imgAsset.asset.src = url;
    imgAsset.asset.onload = () => dispatch(loadSuccess(imgAsset));
    imgAsset.asset.onerror = (error) => { imgAsset.error = error;dispatch(loadFailed(imgAsset));}
}