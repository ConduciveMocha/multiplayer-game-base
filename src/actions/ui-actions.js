import * as UITypes from '../constants/action-types/ui-types';

export const openMessageThread = (threadId) => {
    return {
        type: UITypes.OPEN_MESSAGE_THREAD,
        threadId
    }
};


export const closeMessageThread = (threadId) => {
    return {
        type: UITypes.CLOSE_MESSAGE_THREAD,
        threadId
    };
};

