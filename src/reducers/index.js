import { combineReducers } from "redux";
import loadReducer from "./load-reducer";
import gameReducer from "./game-reducer";
import uiReducer from "./ui-reducer";
import messageReducer from "./message-reducer";
import debugReducer from "./debug-reducer";
import loginStateReducer from "./login-state-reducer";
export default combineReducers({
  ui: uiReducer,
  game: gameReducer,
  assets: loadReducer,
  messaging: messageReducer,
  debug: debugReducer,
  login: loginStateReducer
});
