import {eventChannel, END} from 'redux-saga';
import {take, put, call,all,actionChannel} from 'redux-saga/effects';
import * as SocketActions from '../actions/socket-actions'
import * as SocketTypes from '../constants/action-types/socket-types'
import io from 'socket.io-client';
import * as MessageActions from '../actions/message-actions'
import {appendJwt} from '../api';
import * as MessageTypes from '../constants/action-types/message-types'
// Makes Socket and checks connection
const makeSocket = (url, auth) => {
    try{
        const socket = io(url);
        socket.emit('connect',auth);
        return socket;
    }
    catch(error){
        return null;
    }
}



// Emits actions in response to server pushes
function socketEventChannel(socket) {
    return eventChannel(emitter=>{
        socket.on('connect', ()=>{
            emitter(SocketActions.socketConnected())
        })

        socket.on('error', (error) => {
            emitter(SocketActions.socketFailed(error))
        });

        socket.on('new_message', (data) => {
            emitter(MessageActions.newMessage(data.senderId, data.content,data.timestamp,true))
        })
        
        socket.on('new gamestate', (data) =>{
            // emitter(GameActions.newGameState(data))
        })
        socket.on('update gamestate', (data) => {
            // emitter(GameActions.updateGameState(data))
        })
        return () => {socket.close()}        
    })
}



const createSocketEventHandler = socket => eventType => msg => {
    socket.emit(eventType, JSON.stringify(appendJwt(msg)));
}



const createMessageChannel = socket => {
    const handler = createSocketEventHandler(socket)('new_message');
    return function* () {
        const messageChan = yield actionChannel('MESSAGE_SENT')
        while(true) {
            const action = yield take(messageChan);
            yield call(handler,action)
        }
    }
}


const createEventChannelSaga = socket => {
    return function* (){
        const channel = socketEventChannel(socket)
        while(true) {

            const action = yield take(channel);
            yield put(action);
        }
    }
}


const createMovementChannelSaga = socket => {
    const handler = createSocketEventHandler(socket)('player_movement');
    return function* () {
        const moveChan = yield actionChannel('SEND_MOVEMENT')

        while(true) {
            const action = yield take(moveChan)
            if (action) {yield call(handler,action.movement)};
        }
    }
}

export default function* socketSaga() {
    let socket = null
    while(!socket) {
        let createSocketAction = yield take(SocketTypes.CREATE_SOCKET)
        socket = makeSocket(createSocketAction.url, createSocketAction.auth)
    }

    yield put(SocketActions.socketCreated(socket,'socket'))
    
    
    const movementChannel = createMovementChannelSaga(socket);
    const messageChannel = createMessageChannel(socket);
    const eventChannel = createEventChannelSaga(socket);

    yield all([call(movementChannel),call(messageChannel), call(eventChannel)])
    
}