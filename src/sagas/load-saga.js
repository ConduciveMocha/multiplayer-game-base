import { take, put, call, all, fork } from "redux-saga/effects";

import {
  LOAD_USERS,
  LOAD_THREADS,
  LOAD_THREAD_MESSAGES
} from "../constants/action-types/message-types";
import {
  threadsLoaded,
  usersLoaded,
  threadMessagesLoaded
} from "../actions/load-actions";

import { flaskServer } from "../constants/urls";
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
    yield put(threadsLoaded(threads));
    console.log("Threads Loaded:", threads);
    let thread_messages = yield all(
      threads.map(th => call(jsonPost, th.id, "/load/thread-messages"))
    );
    for (let tm in thread_messages) {
      yield put(threadMessagesLoaded(tm));
    }
  }
}
export default function* loadSaga() {
  yield fork(loadUsers);
  yield fork(loadThreads);
}
