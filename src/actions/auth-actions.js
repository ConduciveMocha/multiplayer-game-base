import * as UiTypes from '../constants/action-types/auth-types';

export const loginSubmitted = (username, password) => {
    const action = {
        type: UiTypes.LOGIN_SUBMITTED,
        username,
        password
    }
    return action
}

export const loginSuccess = (userId) => {
    return { type: UiTypes.LOGIN_SUCCESS, userId }
}

export const loginFailed = (error) => {
    return { type: UiTypes.LOGIN_FAILED, error }
}