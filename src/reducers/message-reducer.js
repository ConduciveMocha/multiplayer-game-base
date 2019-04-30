import * as MessageTypes from "../constants/action-types/message-types";
import Message from "../api/models/message";
import User from "../api/models/user";
import Thread from "../api/models/thread";

const messengerInitialState = {
  threads: new Map([
    ["0", new Thread(0, "Global", [], [], new Date().getTime())]
  ]),
  pendingthreads: [],
  users: {
    friends: new Map([
      ["0", new User(0, "friend1", true)],
      ["1", new User(1, "friend2", true)]
    ]),
    online: new Map()
  }
};

export default function messagingReducer(
  state = messengerInitialState,
  action
) {
  let updatedThreads, updatedUsers, oldThread;
  switch (action.type) {
    case MessageTypes.USER_JOINED:
      updatedUsers = { ...state.users };
      updatedUsers.online.set(action.user.id, action.user);
      return { ...state, users: updatedUsers };

    case MessageTypes.USER_LEFT:
      updatedUsers = { ...state.users };
      updatedUsers.set(action.user.id, action.user);
      return { ...state, users: updatedUsers };

    case MessageTypes.RECIEVE_MESSAGE:
      updatedThreads = { ...state.threads };
      oldThread = updatedThreads.get(action.threadId);
      oldThread.messages.push(action.message);
      updatedThreads.set(action.thread.id, oldThread);

      return { ...state, threads: updatedThreads };

    case MessageTypes.SEND_MESSAGE:
      return { ...state };

    case MessageTypes.MESSAGE_HAS_FAILED:
      return { ...state };

    case MessageTypes.USER_LIST_RECIEVED:
      return { ...state, users: { ...state.users, ...action.userList } };

    default:
      return state;
  }
}
