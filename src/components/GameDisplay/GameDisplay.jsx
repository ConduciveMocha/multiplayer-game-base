import React, { useEffect } from "react";
import { useState } from "react";
import { connect } from "react-redux";
import { playerKeyed } from "../../actions/game-actions";
import "./GameDisplay.css";
const SQUARE = 0;
const TRAPEZOID = 1;
const CIRCLE = 2;

function drawSquare(ctx, x, y) {
  ctx.fillStyle = "deepskyblue";
  ctx.shadowColor = "dodgerblue";
  ctx.shadowBlur = 20;
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + 20, y);
  ctx.lineTo(x + 20, y + 20);
  ctx.lineTo(x, y + 20);
  ctx.lineTo(x, y);
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

function drawTrapezoid(ctx, x, y) {
  ctx.fillStyle = "deeppink";
  ctx.shadowColor = "dodgerblue";
  ctx.shadowBlur = 20;
  ctx.save();

  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + 50, y);
  ctx.lineTo(x + 30, y + 25);
  ctx.lineTo(x - 20, y + 25);
  ctx.lineTo(x, y);
  ctx.fill();

  ctx.stroke();
  ctx.restore();
}

function drawCircle(ctx, x, y) {
  ctx.fillStyle = "salmon";
  ctx.shadowColor = "dodgerblue";
  ctx.shadowBlur = 20;
  ctx.save();
  ctx.moveTo(x, y);
  ctx.beginPath();
  ctx.arc(x, y, 25, 0, 2 * Math.PI);
  ctx.fill();

  ctx.stroke();
}

// const HOOK_SVG =
//   "m129.03125 63.3125c0-34.914062-28.941406-63.3125-64.519531-63.3125-35.574219 0-64.511719 28.398438-64.511719 63.3125 0 29.488281 20.671875 54.246094 48.511719 61.261719v162.898437c0 53.222656 44.222656 96.527344 98.585937 96.527344h10.316406c54.363282 0 98.585938-43.304688 98.585938-96.527344v-95.640625c0-7.070312-4.640625-13.304687-11.414062-15.328125-6.769532-2.015625-14.082032.625-17.960938 6.535156l-42.328125 64.425782c-4.847656 7.390625-2.800781 17.3125 4.582031 22.167968 7.386719 4.832032 17.304688 2.792969 22.160156-4.585937l12.960938-19.71875v42.144531c0 35.582032-29.863281 64.527344-66.585938 64.527344h-10.316406c-36.714844 0-66.585937-28.945312-66.585937-64.527344v-162.898437c27.847656-7.015625 48.519531-31.773438 48.519531-61.261719zm-97.03125 0c0-17.265625 14.585938-31.3125 32.511719-31.3125 17.929687 0 32.511719 14.046875 32.511719 31.3125 0 17.261719-14.582032 31.3125-32.511719 31.3125-17.925781 0-32.511719-14.050781-32.511719-31.3125zm0 0";
// const HOOK_PATH = new Path2D(HOOK_SVG);
const HOOK_PATH = new Path2D();
HOOK_PATH.rect(0, 0, 100, 100);

const SCALE = 0.6;
const OFFSET = [50, 50];
function draw(ctx, gameObject) {
  const { x, y, type } = gameObject;
  ctx.clearRect(0, 0, window.innerWidth * 0.65, window.innerHeight * 0.5);
  switch (type) {
    case CIRCLE:
      drawCircle(ctx, x, y);
      break;
    case TRAPEZOID:
      drawTrapezoid(ctx, x, y);
      break;
    default:
      drawSquare(ctx, x, y);
  }
}
function GameDisplay(props) {
  const displayRef = React.useRef(null);

  useEffect(() => {
    try {
      const canvas = displayRef.current;
      const ctx = canvas.getContext("2d");
      for (let i in props.gameObjects) {
        draw(ctx, props.gameObjects[i]);
      }
    } catch (e) {
      console.log(e);
    }
  }, [props.gameObjects]);

  const handleKeyboardEvent = e => {
    console.log(e.key);
    if (
      e.key === "ArrowLeft" ||
      e.key === "ArrowUp" ||
      e.key === "ArrowDown" ||
      e.key === "ArrowRight"
    ) {
      props.dispatchKeyPress(e.key);
    }
  };

  return (
    <>
      <canvas
        className="game-display"
        ref={displayRef}
        width={window.innerWidth * 0.65}
        height={window.innerHeight * 0.5}
        tabIndex="1"
        onKeyDown={e => handleKeyboardEvent(e)}
      />
    </>
  );
}

export default connect(
  state => ({ gameObjects: state.game.gameObjects }),
  dispatch => ({
    dispatchTest: () => dispatch({ type: "TEST_CANVAS" }),
    dispatchKeyPress: key => dispatch(playerKeyed(key))
  })
)(GameDisplay);
