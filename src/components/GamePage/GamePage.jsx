import React, {useEffect} from 'react';
import GameScreen from './GameScreen'
import DebugLoader from '../DebugLoader'
import {connect} from 'react-redux'
import {withRouter} from 'react-router-dom'
import Messenger from '../Messenger'
const GamePage = (props) =>
{
    useEffect(() => {
        if (!props.showLoader && !props.showGame) {
            console.log(props)
            props.history.push('/')
        }
    })

    return(
        
        <div id='game-page-container'>
            {props.showLoader ? <DebugLoader /> : (
            <div> 
                <GameScreen completed={props.showLoader} />
                <Messenger messageThreads={[]}/>  
            </div>)}
        </div>
    )
}

export default withRouter(connect(state=>{return{showLoader:state.ui.showComponents.loadingScreen, showGame:state.ui.showComponents.gameScreen}}, null)(GamePage));