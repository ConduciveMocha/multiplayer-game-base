import React from 'react';
import GameScreen from './GameScreen'
import DebugLoader from './DebugLoader'


const GamePage = (props) =>
{

    const screen = props.showLoader ? <DebugLoader /> : <GameScreen />

    return(
        <div id='game-page-container'>
            {screen}
        </div>
    )
}