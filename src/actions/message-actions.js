import * as MessageTypes from "../constants/action-types/message-types";

export const sendMessage = (thread, content,) => {
  return {
    type: MessageTypes.SEND_MESSAGE,
    thread,
    content,
    timestamp: new Date().getTime()
  };
};

/**
 * Dispatched when a new message has arrived
 * @param {Message} message - Message object. From json object
 */
export const recieveMessage = message => {
  return {
    type: MessageTypes.RECEIVE_MESSAGE,
  
    message
  };
};

/**
 * Dispatched server signals that the message
 * has been recieved by another user
 * @param {string} memberId - Member id of user that read the message
 * @param {int} messageId -- MessageId in question
 * @param {int} threadId -- ThreadId of message
 * @param {int} timestamp -- Time read by other user. Will be UTC
 */
export const messageWasRecieved = (
  memberId,
  messageId,
  threadId,
  timestamp
) => {
  return {
    type: MessageTypes.MESSAGE_WAS_RECIEVED,
    memberId,
    messageId,
    threadId,
    timestamp
  };
};
/**
 * Dispatched if the server reports an error sending the message.
 * This means that the message was not proccessed correctly by the
 * server or the server didnt respond to the message.
 *
 * @param {int} messageId - Id of failed message
 * @param {int} threadId - Thread of failed message
 * @param {int} timestamp - Utc timestamp (unnecessary?)
 * @param {int} member - memberId that failed to recieve the message
 */
export const messageHasFailed = (
  messageId,
  threadId,
  timestamp,
  member = -1
) => {
  return {
    type: MessageTypes.MESSAGE_HAS_FAILED,
    messageId,
    threadId,
    timestamp,
    member
  };
};
/**
 * Dispatched when the server signals another member has read the message
 * @param {int} memberId - Member who read the message
 * @param {int} messageId - Id of message
 * @param {int} threadId - Thread of message
 * @param {int} timestamp - UTC timestamp
 */
export const messageWasRead = (memberId, messageId, threadId, timestamp) => {
  return {
    type: MessageTypes.MESSAGE_WAS_READ,
    memberId,
    messageId,
    threadId,
    timestamp
  };
};

/**
 * Dispatched by Messenger component when a thread with an unread message
 * has been set to the 'activeThread' (user viewed the thread)
 *
 * @param {int} messageId - message read
 * @param {int} threadId - thread of message
 */
export const reportMessageRead = (messageId, threadId) => {
  return {
    type: MessageTypes.REPORT_MESSAGE_READ,
    messageId,
    threadId,
    timestamp: new Date().getTime()
  };
};

//  TODO: Delete this class. Recieved signal should be handled in saga
export const reportMessageRecieved = (messageId, threadId) => {
  return {
    type: MessageTypes.REPORT_MESSAGE_RECIEVED,
    messageId,
    threadId,
    timestamp: new Date().getTime()
  };
};
/**
 * Dispatched when server reporst a new user has joined
 * @param {User} user - User object of the new user
 * @param {int} timestamp - Time that user joined room. Might be useful for ui?
 */
export const userJoined = (user, timestamp) => {
  return {
    type: MessageTypes.USER_JOINED,
    user,
    timestamp
  };
};

// TODO: asynchronously remove the user's data to avoid a mem leak
/**
 * Dispatched when server reports a user left. Should trigger an async
 * even to clear the user's info from the store.
 * @param {int} userId - id of user that left
 * @param {int} timestamp - Time server reported user left. UI?
 */
export const userLeft = (userId, timestamp) => {
  return {
    type: MessageTypes.USER_LEFT,
    userId,
    timestamp
  };
};

/**
 * Dispatched when a list of users has been recieved. Usually sent on
 * login.
 * @param {list[User]} userList - list of user info
 */
export const userListRecieved = userList => {
  return {
    type: MessageTypes.USER_LIST_RECIEVED,
    userList
  };
};

/**
 * Dispatched when another user attempts to initiate a thread.
 * Allows user to set the thread object in the store
 *
 * @param {Thread} thread - Thread that user is asked to join
 */
export const joinThreadRequest = thread => {
  return {
    type: MessageTypes.JOIN_THREAD_REQUESTED,
    thread
  };
};

/**
 * Dispatched by CreateThread component when user wants to
 * create a new thread.
 * @param {list[int]} members - members to add to thread.
 * @param {string} threadName - User set name for thread. Not required. If not set,
 *                              the server will set it
 * @param {Message} initialMessage - An initial message. As of right now, not required,
 *                             but I might change that
 */
export const requestNewThread = (users, threadName, content) => ( {
    type: MessageTypes.REQUEST_NEW_THREAD,
    name:threadName,
    users:users,
    content:content
  });


export const newThreadFailed = (threadHash, error) => {
  return {
    type: MessageTypes.NEW_THREAD_FAILED,
    threadHash,
    error
  };
};
