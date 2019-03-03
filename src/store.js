import { createStore,applyMiddleware,compose } from "redux";
import createSagaMiddleWare from "redux-saga";
import {assetLoader} from './sagas/load-saga';
import socketSaga from './sagas/socket-saga'
import loadReducer from './reducers/load-reducer';
import testObjs from './api/saga-reducer-test'
import {loadStarted} from './actions/load-actions'

import {createSocket} from './actions/socket-actions'

const composeEnhancers =  window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const loadmw = createSagaMiddleWare()
const socketmw = createSagaMiddleWare()
const store = createStore(loadReducer,{completed:false, gameAssets:[]}, composeEnhancers(applyMiddleware(loadmw,socketmw)
));
loadmw.run(assetLoader);
socketmw.run(socketSaga)
testObjs.forEach((x) => store.dispatch(loadStarted(x)));

store.dispatch(createSocket('http://localhost:5000', 'auth'))

export const dispatch = store.dispatch;
export default store;