import {eventChannel} from 'redux-saga'
import {
    take,
    put,
    call,
    fork
} from "redux-saga/effects"

import * as MessageActions from '.../actions/message-actions';
import * as MessageTypes from '../constants/action-types/message-types';
import {appendJwt} from '../api'
import {connect} from './socket-saga'


const MESSAGING_URL = 'http://localhost:5000/message'


function subscribeToMessageChannel(mSocket) {
    return eventChannel(emit => {
        // Socket event handlers go here
        mSocket.on("NEW_MESSAGE", (payload)=>{

        })
        mSocket.on("MESSAGE_FAILED",(payload)=>{})

        mSocket.on("")
        // Unsubscribe to Socket
        return () => {}
    });

}

function* readMessageChannel(mSocket) {
    const messageChannel = yield call(subscribeToMessageChannel, mSocket);
    while (true) {
        let action = yield take(messageChannel);
        switch(action) {

        }
    }
}

function* write(mSocket) {
    while(true) {
        const {payload} = yield take()
    }
}

function* messagingFlow() {
    while(true) {
        const socket = yield call(connect,)   
    }
}