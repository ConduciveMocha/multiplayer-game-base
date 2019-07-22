import { combineReducers } from "redux";
import loadReducer from "./load-reducer";
import gameReducer from "./game-reducer";
import uiReducer from "./ui-reducer";
import messagingReducer from "./message-reducer";
import debugReducer from "./debug-reducer";
export default combineReducers({
  ui: uiReducer,
  game: gameReducer,
  assets: loadReducer,
  messaging: messagingReducer,
  debug: debugReducer
});
