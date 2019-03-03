import * as SocketTypes from '../constants/action-types/socket-types';
import { Socket } from 'net';

export const createSocket = (url, auth) => {
    return {
        type: SocketTypes.CREATE_SOCKET,
        url,
        auth
    }
}

export const socketCreated = (socket, connectionName="default") => {
    return {
        type: SocketTypes.SOCKET_CREATED,
        socket,
        connectionName
    }
}

export const socketFailed = (error) => {
    return {
        type: SocketTypes.SOCKET_FAILED,
        error
    }
}

export const socketConnected = () => {
    return {
        type:SocketTypes.SOCKET_CONNECTED
    }
}

export const closeSocket = (socket) => {
    return {
        type:SocketTypes.CLOSE_SOCKET,
        socket
    }
}

export const socketClosed = () => {
    return {
        type:SocketTypes.SOCKET_CLOSED
    }
}

export const socketCloseDelayed = (timeout, error) => {
    return {
        type: SocketTypes.SOCKET_CLOSE_DELAYED,
        timeout,
        error
    }
}

