const socketLogger = {
  sent: (eventType, payload) =>
    console.log("SENT::SOCKETEVENT::" + eventType, "payload:", payload),
  recieved: (eventType, payload) =>
    console.log("RECIEVED::SOCKETEVENT::" + eventType, "payload:", payload),
  redux: (eventType, payload) =>
    console.log("REDUX::SOCKETEVENT::" + eventType, "payload:", payload),
  error: (eventType, payload) =>
    console.log(
      "ERROR::SOCKETEVENT::" + eventType,
      "message:",
      payload.errorMessage
    )
};
export default socketLogger;
