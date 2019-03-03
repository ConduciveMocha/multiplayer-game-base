import React, {useState} from 'react';
import PropTypes from 'prop-types';
import sprite from '../assets/player-sprites/sprite1_front.png';
import { throws } from 'assert';

import {connect} from 'react-redux'

class GameScreen extends React.Component {
    constructor(props){
        super(props);
      //  this.hasLoaded = false;
       // this.divSize = this.props.width / this.props.gridDim.x;
        
    }

    cellsToPixels = index => index * this.divSize;

    

    componentDidUpdate() {
        this.ctx = this.refs.canvas.getContext('2d');
        this.drawGameState()

    }

    componentDidMount() {
        this.ctx  = this.refs.canvas.getContext('2d');
        this.drawGameState();
    }






    drawGameState() {  
        if (this.props.completed)
            this.ctx.drawImage(this.props.gameAssets[1].asset, 0,0);
        return;


    }



    

    render() {
        return(
            <div id='game-screen-container'>
                <canvas ref='canvas' width={this.props.width} height={this.props.height}></canvas>
            </div>
        )
    }
}


// GameScreen.propTypes={
//     width: PropTypes.number,
//     height: PropTypes.number
// };

// const mapStateToProps = (state) => {
//    return  {
//        gameState: state.gameState
        
//     }
// }



export default connect(
    state=>{return {gameAssets:state.gameAssets}},
    null
)(GameScreen);