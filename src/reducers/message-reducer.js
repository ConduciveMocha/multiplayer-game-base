import * as MessageTypes from "../constants/action-types/message-types";
import Message from "../api/models/message";
import User from "../api/models/user";
import Thread from "../api/models/thread";

/**
 * Data Model:
 * threads:Map()             --> Thread Identifier to thread object
 * users: {
 *  friends: Map()
 *  online: Map()
 * }            --> User identifier to user object
 * openThreads:Set()     --> Members are some thread Identifier
 * shownTabIndex:int      --> Thread Identifier
 * newThreadScreens:Set() --> Members are thread identifier
 * activeThread:int/String   --> Some thread Identifier
 *
 */

const messengerInitialState = {
  threads: new Map([
    ["0", new Thread(0, "Global", [], [], new Date().getTime())]
  ]),

  users: {
    friends: new Map([
      ["0", new User(0, "friend1", true)],
      ["1", new User(1, "friend2", true)]
    ]),
    online: new Map()
  },
  openThreads: [0],
  shownTabIndex: 0,
  newThreadScreens: new Map(),
  activeThread: 0
};

export default function messagingReducer(
  state = messengerInitialState,
  action
) {
  switch (action.type) {
    // SERVER ACTIONS
    case MessageTypes.SEND_MESSAGE:
      return { ...state };
    case MessageTypes.RECIEVE_MESSAGE:
      return { ...state };

    case MessageTypes.MESSAGE_HAS_FAILED:
      return { ...state };
    case MessageTypes.MESSAGE_WAS_RECIEVED:
      return { ...state };
    case MessageTypes.MESSAGE_WAS_READ:
      return { ...state };

    case MessageTypes.USER_JOINED:
      return { ...state };
    case MessageTypes.USER_LEFT:
      return { ...state };

    case MessageTypes.USER_LIST_RECIEVED:
      return { ...state };

    case MessageTypes.NEW_THREAD_ACCEPTED:
      return { ...state };

    // UI Actions
    case MessageTypes.THREAD_OPENED:
      return { ...state };
    case MessageTypes.THREAD_CLOSED:
      return { ...state };
    case MessageTypes.NEW_THREAD_SCREEN:
      return { ...state };
    case MessageTypes.NEW_THREAD_CLOSED:
      return { ...state };
    case MessageTypes.USER_ADDED_TO_THREAD:
      return { ...state };
    case MessageTypes.CLOSE_ALL_THREADS:
      return { ...state };

    case MessageTypes.ACTIVE_THREAD_CHANGED:
      return {
        ...state
      };
    case MessageTypes.OPEN_GLOBAL:
      return {
        ...state,
        activeThread: state.openThreads[0],
        shownTabIndex: 0
      };
    case MessageTypes.NAVIGATE_LEFT:
      return {
        ...state,
        shownTabIndex:
          shownTabIndex > 1 ? shownTabIndex - 1 : state.shownTabIndex
      };
    case MessageTypes.NAVIGATE_RIGHT:
      return {
        ...state,
        shownTabIndex:
          shownTabIndex < state.openThreads.length - 1
            ? state.shownTabIndex + 1
            : state.shownTabIndex
      };
    //
    default:
      return state;
  }
}
