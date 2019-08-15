import * as UserTypes from "../constants/action-types/user-types";

/**
 *                  login ->
 *                           <- Return UserId
 *                           <- Return JWT
 * request User Info Load ->
 *                           <- Returns user info
 * request thread history ->
 *                           <- returns thread history
 */

const testUserState = {};
export default function userReducer(state = testUserState, action) {
  switch (action.type) {
    case UserTypes.LOAD_USER_DATA:
      return { ...state };

    default:
      return { ...state };
  }
}
