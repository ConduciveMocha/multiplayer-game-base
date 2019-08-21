import { put, take, call, takeEvery } from "redux-saga/effects";
// import {submitLogin} from '../api/login'
import { LOGIN_SUBMITTED } from "../constants/action-types/auth-types";
import { loginSuccess, loginFailed } from "../actions/auth-actions";
// import { startInitialLoad } from "../actions/load-actions";

const submitLogin = () => {
  console.error('Function "submitLogin" is not implemented');
};

function* submitLoginSaga(action) {
  const loginResponse = yield call(
    submitLogin,
    action.username,
    action.password
  );
  if (loginResponse.error) {
    yield put(loginFailed(loginResponse.error));
    return null;
  } else return loginResponse.jwt.user_id;
}

export default function* authSaga() {
  let userId = null;
  while (!userId) {
    const action = yield take(LOGIN_SUBMITTED);
    userId = yield call(submitLoginSaga, action);
  }

  yield put(loginSuccess(userId));
  // yield put(startInitialLoad());
}
