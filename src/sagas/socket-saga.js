import {eventChannel, END} from 'redux-saga';
import {take, put, call,all,actionChannel} from 'redux-saga/effects';
import * as SocketActions from '../actions/socket-actions'
import * as SocketTypes from '../constants/action-types/socket-types'
import io from 'socket.io-client';

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

        socket.on('new gamestate', (data) =>{
            // emitter(GameActions.newGameState(data))
        })
        socket.on('update gamestate', (data) => {
            // emitter(GameActions.updateGameState(data))
        })
        socket.on('private message', (data) => {
            console.log('here')
            console.log(data)
            // emitter(MessageActions.privateMessageRecieved)
        })
        socket.on('global message', (data) => {
            // emitter(MessageActions.globalMessageRecieved)
        })
        return () => {socket.close()}        
    })
}

const createMessageHandler = socket => msg => {
    socket.send(JSON.stringify(msg))
}

const createMovementHandler = socket => movement => {
    socket.send(JSON.stringify(movement))
}

const createEventChannelSaga = socket => {
    return function* (){
        const channel = socketEventChannel(socket)
        while(true) {
            console.log('3')

            const action = yield take(channel);
            yield put(action);
        }
    }
}

const createMessageChannelSaga = socket => {
    const handler = createMessageHandler(socket);
    return function* () {
        const messageChan = yield actionChannel('SEND_MESSAGE')
        while(true) {
            const action = yield take(messageChan);
            yield call(handler,action.msg)
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

    yield put(SocketActions.socketConnected())
    console.log('there')
    socket.emit('private message', JSON.stringify({data:'abcd'}))
    const movementChannel = createMovementChannelSaga(socket);
    const messageChannel = createMessageChannelSaga(socket);
    const eventChannel = createEventChannelSaga(socket);

    yield all([call(movementChannel),call(messageChannel), call(eventChannel)])
    
}