import { createStore, applyMiddleware, compose } from "redux";
import createSagaMiddleWare from "redux-saga";
import { assetLoader } from "./sagas/load-saga";
import socketSaga from "./sagas/socket-saga";
import authSaga from "./sagas/auth-saga";
import rootReducer from "./reducers";
// import testObjs from './api/saga-reducer-test'
import { loadStarted, startInitialLoad } from "./actions/load-actions";

import { flaskServer } from "./constants/urls";
import { createSocket } from "./actions/socket-actions";

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const loadMw = createSagaMiddleWare();
const socketMw = createSagaMiddleWare();
const authMw = createSagaMiddleWare();
const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(loadMw, socketMw, authMw))
);

loadMw.run(assetLoader);
socketMw.run(socketSaga);
authMw.run(authSaga);
store.dispatch(createSocket(flaskServer, "auth"));

export const dispatch = store.dispatch;
export default store;
