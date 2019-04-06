import * as MessageTypes from "../constants/action-types/message-types";
const thisUser = { userId: "1", username: "username" };

let _users = {};
_users[thisUser.userId] = thisUser.username;
const messengerInitialState = {
  threads:{"1":{threadId:1},"2":{threadId:2}},
  users: {"1":{id:thisUser.userId, username:thisUser.username,online:true}}
};

function makeMessage(action){
  return {
    threadId: action.threadId,
    senderId: action.senderId,
    timestamp: action.timestamp,
    content: action.content
  };
}

export default function messagingReducer(state=messengerInitialState, action) {
  let updatedThreads, updatedUsers;
  switch (action.type) {
    case MessageTypes.USER_JOINED:
      updatedUsers =  {...state.users}
      updatedUsers[action.userId] = {id:action.userId,username:action.username, online:true }
      return {...state, users:updatedUsers}    

    case MessageTypes.USER_LEFT:
      updatedUsers = {...state.users};
      updatedUsers[action.userId].online = false;
      return {...state, users:updatedUsers}

    case MessageTypes.NEW_MESSAGE:
    
      updatedThreads = {...state.threads}
      updatedThreads[action.threadId].messages.push(makeMessage(action));
      updatedThreads[action.threadId].hasUnread = true;

      return {...state, threads:updatedThreads}
  
    case MessageTypes.MESSAGE_SENT:
      updatedThreads = { ...state.threads }
      updatedThreads[action.threadId].messages.push(makeMessage(action));
      return { ...state, threads: updatedThreads }
  
    case MessageTypes.MESSAGE_FAILED:
      return {...state}    

    case MessageTypes.USER_LIST_RECIEVED:
      return {...state, users:{...state.users,...action.userList}}
        
    default:
      return state;
  }
}



