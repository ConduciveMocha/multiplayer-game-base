import * as MessageTypes from "../constants/action-types/message-types";
const MESSAGE_STATUS = {
  SENT: 2,
  RECIEVED: 1,
  FAILED: 0
};

const messengerInitialState = {
  threads: {},
  users: {},
  onlineUserIds: [],
  friendsListIds: [],
  messages: {}
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

    case MessageTypes.RECIEVE_MESSAGE:
      return {
        ...state,
        messages: {
          ...state.messages,
          [action.message.messageId]: action.message // Adds message to message hash
        },
        threads: {
          ...state.threads,
          [action.message.threadId]: [
            // Adds MessageId to appropriate thread
            ...state[action.message.threadId],
            action.message.messageId
          ]
        }
      };

    case MessageTypes.SEND_MESSAGE:
      return {
        ...state,
        messages: {
          ...state.messages,
          [action.message.messageId]: {
            ...action.message,
            status: MESSAGE_STATUS.SENT
          } // Adds message to message hash
        },
        threads: {
          ...state.threads,
          [action.message.threadId]: [
            // Adds MessageId to appropriate thread
            ...state[action.message.threadId],
            action.message.messageId
          ]
        }
      };

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
