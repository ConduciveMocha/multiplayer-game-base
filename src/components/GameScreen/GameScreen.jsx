import React from 'react';

import Messenger from '../Messenger';
import GameDisplay from '../GameDisplay';
import InventorySidebar from '../InventorySidebar';

const GameScreen = (props) => {
    return (
        <div>
            <div>
                <InventorySidebar/>
                <GameDisplay />
            </div>
            <Messenger />
        </div>
    )
}

export default GameScreen;