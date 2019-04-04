import {eventChannel, END} from 'redux-saga';
import {take, put, call,all,actionChannel} from 'redux-saga/effects';
import * as SocketActions from '../actions/socket-actions'
import * as SocketTypes from '../constants/action-types/socket-types'
import io from 'socket.io-client';
import * as MessageActions from '../actions/message-actions'

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

        socket.on('private message', (data) => {
            emitter(MessageActions.newMessage(data.senderId, data.content,data.timestamp,true))
        })
        socket.on('global message', (data) => {
            emitter(MessageActions.newMessage(data.senderId,data.content,data.timestamp,false))
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
const createMovementHandler = socket => movement => {
    socket.send(JSON.stringify(movement))
}

const createMessageHandler = socket => msg => {
            if (msg.isPrivate)
              socket.eemit("private message",JSON.stringify(msg));
            else
              socket.emit("global message", JSON.stringify(msg));}


const createMessageInterceptChannel = socket => {
    const handler = createMessageHandler(socket);
    return function* () {
        const messageChan = yield actionChannel('MESSAGE_SENT')
        while(true) {
            const action = yield take(messageChan);
            console.log(action)
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
    const handler = createMovementHandler(socket);
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
    // socket.emit('private message', JSON.stringify({data:'abcd'}))
    const movementChannel = createMovementChannelSaga(socket);
    const messageChannel = createMessageInterceptChannel(socket);
    const eventChannel = createEventChannelSaga(socket);

    yield all([call(movementChannel),call(messageChannel), call(eventChannel)])
    
}