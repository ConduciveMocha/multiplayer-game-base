export default function debugReducter(state = { last: "" }, action) {
  switch (action.type) {
    case "TEST_ACTION":
      return { last: action.data };
    default:
      return state;
  }
}
