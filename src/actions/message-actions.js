import * as MessageTypes from '../constants/action-types/message-types'

export const messageSent = (userId, threadId, content) => {
    return {
        type: MessageTypes.MESSAGE_SENT,
        userId,
        threadId,
        content,
        timestamp: new Date().getTime()
    }
}

export const messageFailed = (messageId,threadId, timestamp) => {
    return {
        type: MessageTypes.MESSAGE_FAILED,
        messageId,
        threadId,
        timestamp
    }
}

export const newMessage = (senderId,threadId,content,timestamp) => {
    return {
        type: MessageTypes.NEW_MESSAGE,
        senderId,
        threadId,
        content,
        timestamp
    }
}

export const messageRecieved = (messageId,threadId, timestamp) => {
    return {
        type: MessageTypes.MESSAGE_RECIEVED,
        messageId,
        threadId,
        timestamp
    }
}

export const messageRead = (messageId, threadId, timestamp) => {
    return {
        type: MessageTypes.MESSAGE_READ,
        messageId,
        threadId, 
        timestamp
    }
}

export const reportMessageRead = (messageId, threadId) => {
    return {
        type: MessageTypes.REPORT_MESSAGE_READ,
        messageId,
        threadId,
        timestamp: new Date().getTime()
    }
}

export const reportMessageRecieved = (messageId, threadId) => {
    return {
        type: MessageTypes.REPORT_MESSAGE_RECIEVED,
        messageId,
        threadId,
        timestamp: new Date().getTime()
    }
}

export const userJoined = (userId,username,timestamp) => {
    return {
        type: MessageTypes.USER_JOINED,
        userId,
        username,
        timestamp
    }
};

export const userLeft = (userId,timestamp) => {
    return {
        type: MessageTypes.USER_LEFT,
        userId,
        timestamp
    }
};

export const userListRecieved = (userList) => {
    return {
        type: MessageTypes.USER_LIST_RECIEVED,
        userList
    }
}