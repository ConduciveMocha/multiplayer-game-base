import React from "react";

const MessageItem = message => {
  return (
    <div
      className={
        message.userSent ? "mesesage-item-sent" : "message-item-received"
      }
    >
      <p className="item-username">message.sender.username</p>
      <div className="message-item-content">{message.markup}</div>
      <p className="message-item-timestamp">message.created</p>
    </div>
  );
};
// Needs Props:
// -messageList: [message]
export const MessageDisplay = props => {
  let messageItems = props.messageList.map(message => MessageItem(message));
  return <ul classNam="message-display-container">{messageItems}</ul>;
};

export default MessageDisplay;
