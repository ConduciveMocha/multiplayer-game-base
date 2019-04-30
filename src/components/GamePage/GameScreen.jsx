import React, { useState } from "react";
import PropTypes from "prop-types";
import { throws } from "assert";

import { connect } from "react-redux";
class GameScreen extends React.Component {
  constructor(props) {
    super(props);
  }

  cellsToPixels = index => index * this.divSize;

  componentDidUpdate() {
    this.ctx = this.refs.canvas.getContext("2d");
    this.drawGameState();
  }

  componentDidMount() {
    this.ctx = this.refs.canvas.getContext("2d");
    this.drawGameState();
  }

  drawGameState() {
    this.ctx.drawImage(this.props.gameAssets[1].asset, 0, 0);
  }

  render() {
    return (
      <div id="game-screen-container">
        <canvas
          ref="canvas"
          width={this.props.width}
          height={this.props.height}
        />
      </div>
    );
  }
}

export default connect(
  state => {
    return { gameAssets: state.assets.gameAssets };
  },
  null
)(GameScreen);
