import {SOCKET_CREATED} from './constants/action-types/socket-types';
import {socketConnected} from './actions/socket-actions'
const createSocketMiddleware = ()=> { 
    let socket=null;
    
    return store => next => action =>{
        if(socket) {
            
        }
        else if (action.type === SOCKET_CREATED) {
            socket = action.socket;
            socket.on('new gamestate', (gameState)=>{
                // store.dispatch(GameActions.updateGameState(gameState))
            })
            return next(socketConnected());

        }
    }
}
