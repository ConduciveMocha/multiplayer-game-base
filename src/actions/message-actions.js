import * as MessageTypes from '../constants/action-types/message-types'

export const messageSent = (recipientId, content, timestamp) => {
    return {
        type: MessageTypes.MESSAGE_SENT,
        timestamp,
        recipientId,
        content
    }
}

export const messageFailed = (recipientId,content, timestamp) => {
    return {
        type: MessageTypes.MESSAGE_FAILED,
        recipientId,
        content,
        timestamp
    }
}

export const newMessage = (senderId,content,timestamp,isPrivate=false) => {
    return {
        type: MessageTypes.NEW_MESSAGE,
        timestamp,
        senderId,
        content,
        isPrivate
    }
}