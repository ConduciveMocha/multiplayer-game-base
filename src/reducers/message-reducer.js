import * as MessageTypes from "../constants/action-types/message-types";
const thisUser = { userId: "1", username: "username" };

let _users = {};
_users[thisUser.userId] = thisUser.username;
const messengerInitialState = {
  users: {..._users, "0":true},
  threads: {"0": []},
  failed: {},
  lastSent: "0"
};


export default function messagingReducer(state = messengerInitialState, action) {
  let newMessage, failedMessage,updatedThreads, updatedErrors;
  switch (action.type) {

   case MessageTypes.NEW_MESSAGE:

       newMessage = {
          senderId: action.senderId,
          content: action.content,
          timestamp: action.timestamp
      };
      updatedThreads = { ...state.threads };
      if (action.isPrivate) {
          updatedThreads[action.senderId] = state.threads[action.senderId]? [newMessage, ...state.threads[action.senderId].slice(1)]: [newMessage];
      } 
      else if (!action.isPrivate) {
          updatedThreads["0"] = state.threads["0"]? [newMessage, ...state.threads["0"].slice(1)]: [newMessage];
      }  
      return {...state,threads:updatedThreads,lastSent:action.senderId}
  
  case MessageTypes.MESSAGE_SENT:
      newMessage = {
          senderId: thisUser.userId,
          content: action.content,
          timestampe:action.timestamp
      }
      updatedThreads = {...state.threads}
      updatedThreads[action.recipientId] = state.threads[action.recepientId] 
        ? [newMessage,...state.threads[action.recipientId]] 
        : [newMessage] 
      
      return { ...state, threads: updatedThreads, lastSent:action.recipientId };
  
  case MessageTypes.MESSAGE_FAILED:
      failedMessage = {
          senderId: thisUser.userId,
          content: action.content,
          timestamp:action.timestamp
      }

      updatedErrors = {...state.errors}
      updatedErrors[action.recepientId] = state.failed[action.recepientId]
        ? [failedMessage,...state.failed[action.recepientId]]
        : [failedMessage]
      return {...state, failed:updatedErrors}
  
  
      default:
    return state;
  }
}




// export default function messagingReducer(state = messengerInitialState, action) {
//     let newMessage, failedMessage,updatedThreads, updatedErrors;
//     switch (action.type) {
//     // case MessageTypes.USER_JOINED:
//     //   let updatedUsers = state.users.slice();
//     //   updatedUsers[action.userId] = action.username;
//     //   return { ...state, users: updatedUsers };
//     // case MessageTypes.USER_LEFT:
//     //   let updatedUsers = state.users.slice();
//     //   updatedUsers[action.userId] = null;
//     //   return { ...state, users: updatedUsers };
//      case MessageTypes.NEW_MESSAGE:

//          newMessage = {
//             senderId: action.senderId,
//             content: action.content,
//             timestamp: action.timestamp
//         };
//         updatedThreads = { ...state.threads };
//         if (action.isPrivate) {
//             updatedThreads[action.senderId] = state.threads[action.senderId]? [newMessage, ...state.threads[action.senderId].slice(1)]: [newMessage];
//         } 
//         else if (!action.isPrivate) {
//             updatedThreads["0"] = state.threads["0"]? [newMessage, ...state.threads["0"].slice(1)]: [newMessage];
//         }  
//         return {...state,threads:updatedThreads,lastSent:action.senderId}
    
//     case MessageTypes.MESSAGE_SENT:
//         newMessage = {
//             senderId: thisUser.userId,
//             content: action.content,
//             timestampe:action.timestamp
//         }
//         updatedThreads = {...state.threads}
//         updatedThreads[action.recipientId] = state.threads[action.recepientId] 
//           ? [newMessage,...state.threads[action.recipientId]] 
//           : [newMessage] 
        
//         return { ...state, threads: updatedThreads, lastSent:action.recipientId };
    
//     case MessageTypes.MESSAGE_FAILED:
//         failedMessage = {
//             senderId: thisUser.userId,
//             content: action.content,
//             timestamp:action.timestamp
//         }

//         updatedErrors = {...state.errors}
//         updatedErrors[action.recepientId] = state.failed[action.recepientId]
//           ? [failedMessage,...state.failed[action.recepientId]]
//           : [failedMessage]
//         return {...state, failed:updatedErrors}
    
    
//         default:
//       return state;
//     }
// }