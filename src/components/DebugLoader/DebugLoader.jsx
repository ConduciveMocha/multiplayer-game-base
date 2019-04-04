import React, {useState,useEffect} from 'react';
import {connect} from 'react-redux';
import './debug-loader.css';
// import LoadStates from '../constants/LoadStates'
// import * as LoadActions from '../actions/load-actions'
// import testObjects from '../api/saga-reducer-test';

const ListItem = (props) => {
    return (
        <li className={['failed','successful','loading','pending'][props.gameAsset.loadState]}>
        {props.gameAsset.assetUrl}
        </li>

    )
}

const DebugLoader = (props) => {
    const assetList = props.assetList;
   const assetElements = assetList.map(x=> {
        return (<ListItem key={x.id} gameAsset={x}/>)
        
    });

    return(
        <div id='load-container'>
    
            <ul id='asset-load-list'>
                {assetElements}  
            </ul>
        
        </div>
    )

}


export default connect(
    state=> {return {assetList: state.assets.gameAssets}},
    null
    )(DebugLoader);