import * as MessageTypes from "../constants/action-types/message-types";
import { mockThreads,mockMessages,mockUsers,mockFriendsList,mockOnlineUserIds } from "../utils/messaging-mock";

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
  messages: mockMessages
};

export default function messagingReducer(
  state = messengerInitialState,
  action
) {


  switch (action.type) {
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
      console.log('Messaging reducer:', 'RECIEVE_MESSAGE',action)
      console.log('state', state)
      let message = action.message;
      let updatedThread = {...state.threads[action.message.thread]}
      updatedThread.messages = [...updatedThread.messages,message.id]
      let newState = {
        ...state, 
        messages:{...state.messages,[message.id]:message},
        threads:{...state.threads, [action.message.thread]:updatedThread} 
      }
      console.log('new state', newState) 
      return newState


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

    default:
      return state;
  }
}
