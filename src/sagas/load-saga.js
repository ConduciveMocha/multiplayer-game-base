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
import { LOAD_GAME_OBJECTS } from "../constants/action-types/load-types";

import { jsonPost } from "../api";

function* loadUsers() {
  while (true) {
    const action = yield take(LOAD_USERS);
    let users = yield call(jsonPost, action, "/load/user-list");
    yield put(usersLoaded(users));
  }
}

function* loadThreads() {
  while (true) {
    const action = yield take(LOAD_THREADS);
    let threads = yield call(jsonPost, action, "/load/threads");
    threads = threads.threads;
    let thread_messages = yield all(
      Object.values(threads).map(th =>
        call(jsonPost, { thread: th.id }, "/load/thread-messages")
      )
    );

    for (let th in threads) {
      yield put({ type: CLIENT_THREAD_REQUEST, thread: threads[th].id });
    }
    for (let tm in thread_messages) {
      console.log(threadMessagesLoaded(thread_messages[tm].messages));
      yield put(threadMessagesLoaded(thread_messages[tm].messages));
    }
    yield put(threadsLoaded(threads));
  }
}

function* loadGameObjects() {
  while (true) {
    const action = yield take(LOAD_GAME_OBJECTS);
    let game_objects_resp = yield call(jsonPost, action, "/load/game-objects");
  }
}

export default function* loadSaga() {
  yield fork(loadUsers);
  yield fork(loadThreads);
}
