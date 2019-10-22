import { createStore, applyMiddleware, compose } from "redux";
import createSagaMiddleWare from "redux-saga";
import { messageIO } from "./sagas/socket-sagas/message-socket-saga";
import socketSaga from "./sagas/socket-saga";
import authSaga from "./sagas/auth-saga";
import loadSaga from "./sagas/load-saga";
import rootReducer from "./reducers";

// import testObjs from './api/saga-reducer-test'
import { loadStarted, startInitialLoad } from "./actions/load-actions";

import { flaskServer } from "./constants/urls";
import { createSocket } from "./actions/socket-actions";

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const socketMw = createSagaMiddleWare();
const authMw = createSagaMiddleWare();
const messageMw = createSagaMiddleWare();
const loadMw = createSagaMiddleWare();
const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(socketMw, authMw, messageMw, loadMw))
);

socketMw.run(socketSaga);
authMw.run(authSaga);
messageMw.run(messageIO);
loadMw.run(loadSaga);
store.dispatch(createSocket(flaskServer, "auth"));

export const dispatch = store.dispatch;
export default store;
