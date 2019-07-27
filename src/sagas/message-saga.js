
import {
    take,
    put,
    call,
    fork
} from "redux-saga/effects"

import * as MessageTypes from '../constants/action-types/message-types';
import {appendJwt,jsonPost} from '../api'


const MESSAGING_URL = 'http://localhost:5000/message'

export default function* requestThreadSaga(action) {
    while(true){
        
        const action = yield take(MessageTypes.REQUEST_NEW_THREAD);
        console.log('requestThreadSaga:')
        console.log('Action: ', action)
        let requestThreadResp = yield call(jsonPost,action, '/message/requestnewthread');
        console.log('Response: ', requestThreadResp)
    }


}
