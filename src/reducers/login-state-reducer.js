import User from "../api/models/user";

export default function loginStateReducer(
  state = { clientUser: new User(0, "this-user", true) },
  action
) {
  switch (action.type) {
    default:
      return state;
  }
}
