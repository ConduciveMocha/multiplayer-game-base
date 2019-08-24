import { take, put, call, all, fork } from "redux-saga/effects";

import {
  LOAD_USERS,
  LOAD_THREADS,
  LOAD_THREAD_MESSAGES,
  REQUEST_THREAD_JOIN,
  SERVER_THREAD_REQUEST,
  CLIENT_THREAD_REQUEST
} from "../constants/action-types/message-types";
import {
  threadsLoaded,
  usersLoaded,
  threadMessagesLoaded
} from "../actions/load-actions";
import {LOAD_GAME_OBJECTS} from '../constants/action-types/load-types'

import { jsonPost } from "../api";

function* loadUsers() {
  while (true) {
    const action = yield take(LOAD_USERS);
    console.log("LOAD_USERS CALLED", action);
    let users = yield call(jsonPost, action, "/load/user-list");
    console.log("Response: ", users);
    yield put(usersLoaded(users));
  }
}

function* loadThreads() {
  while (true) {
    const action = yield take(LOAD_THREADS);
    console.log("LOAD_THREADS Called", action);
    let threads = yield call(jsonPost, action, "/load/threads");
    threads = threads.threads
    console.log("Threads Loaded:", threads);
    let thread_messages = yield all(
      Object.values(threads).map(th => call(jsonPost, {thread:th.id}, "/load/thread-messages"))
      );

      for(let th in threads){
        console.log('Th in threads', th)
        yield put({type:CLIENT_THREAD_REQUEST, thread:threads[th].id})
      }
      console.log('Thread Messages',thread_messages)
      for (let tm in thread_messages) {
        console.log(threadMessagesLoaded(thread_messages[tm].messages))
        yield put(threadMessagesLoaded(thread_messages[tm].messages));
      }
      yield put(threadsLoaded(threads));
  }
}

function* loadGameObjects() {
  while(true){
    const action = yield take(LOAD_GAME_OBJECTS)
    console.log('LOAD_GAME_OBJECTS CALLED')
    let game_objects_resp = yield call(jsonPost,action,'/load/game-objects')
    console.log('Game objects response: ', game_objects_resp)
    

  }
}


export default function* loadSaga() {
  yield fork(loadUsers);
  yield fork(loadThreads);
}
