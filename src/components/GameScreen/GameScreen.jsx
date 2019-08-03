import React from "react";

import Messenger from "../Messenger";
import GameDisplay from "../GameDisplay";
import InventorySidebar from "../InventorySidebar";
import "./GameScreen.css";
const GameScreen = props => {
  return (
    <div>
      <div className="game-container">
        <InventorySidebar />
        <GameDisplay />
      </div>
      <Messenger />
    </div>
  );
};

export default GameScreen;
