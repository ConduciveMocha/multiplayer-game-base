import * as MessageTypes from "../constants/action-types/message-types";
import {
  mockThreads,
  mockMessages,
  mockUsers,
  mockFriendsList,
  mockOnlineUserIds
} from "../utils/messaging-mock";

const MESSAGE_STATUS = {
  SENT: 2,
  RECIEVED: 1,
  FAILED: 0
};

const messengerInitialState = {
  threads: mockThreads,
  users: mockUsers,
  onlineUserIds: mockOnlineUserIds,
  friendsList: mockFriendsList,
  messages: mockMessages,
  newThreadId: null
};

export default function messagingReducer(
  state = messengerInitialState,
  action
) {
  let newState;
  switch (action.type) {
    case MessageTypes.USERS_LOADED:
      console.log("USERS_LOADED", action);
      return {
        ...state,
        users: { ...action.online, ...action.friends },
        friendsList: [...Object.keys(action.friends).map(id => parseInt(id))],
        onlineUserIds: [...Object.keys(action.online).map(id => parseInt(id))]
      };

    case MessageTypes.THREADS_LOADED:
      return {
        ...state,
        threads: { ...state.threads, ...action.threads }
      };

    case MessageTypes.THREAD_MESSAGES_LOADED:
      console.log('THREAD_MESSAGES_LOADED','OLD',state)
      newState = {
        ...state,
        messages: {
          ...state.messages,
          ...action.messages
        }
      }
        console.log('THREAD_MESSAGES_LOADED','NEW',newState)
      return newState;
    
    case MessageTypes.USER_JOINED:
      return {
        ...state,
        users: { ...state.users, [action.user.userId]: action.user },
        onlineUserIds: [...state.onlineUserIds, action.user.userId]
      };

    case MessageTypes.USER_LEFT:
      let removedUserState = { ...state };
      delete removedUserState[action.user.userId];
      let updatedOnlineUserIds = state.onlineUserIds.filter(
        el => el !== action.user.userId
      );
      return { ...removedUserState, onlineUserIds: updatedOnlineUserIds };

    case MessageTypes.RECEIVE_MESSAGE:
      console.log("Messaging reducer:", "RECIEVE_MESSAGE", action);
      console.log("state", state);
      let message = action.message;
      let updatedThread = { ...state.threads[action.message.thread] };
      updatedThread.messages = [...updatedThread.messages, message.id];
      let newState = {
        ...state,
        messages: { ...state.messages, [message.id]: message },
        threads: { ...state.threads, [action.message.thread]: updatedThread }
      };
      console.log("new state", newState);
      return newState;

    case MessageTypes.MESSAGE_HAS_FAILED:
      return {
        ...state,
        // Sets message status to failed
        messages: {
          ...state.messages,
          [action.message.messageId]: {
            ...state.messages[action.message.messageId],
            status: MESSAGE_STATUS.FAILED
          }
        }
      };

    case MessageTypes.USER_LIST_RECIEVED:
      return {
        ...state,
        // Sets message status to recieved
        messages: {
          ...state.messages,
          [action.message.messageId]: {
            ...state.messages[action.message.messageId],
            status: MESSAGE_STATUS.RECIEVED
          }
        }
      };

    case MessageTypes.SERVER_THREAD_REQUEST:
      return {
        ...state,
        threads: { ...state.threads, [action.thread.id]: action.thread },
        newThreadId: action.thread.id
      };

    case MessageTypes.CLEAR_NEW_THREAD:
      return { ...state, newThreadId: null };

    default:
      return state;
  }
}
