import React from "react";

const Message = (text, sender) => {
  return (
    <div className="message">
      <div className={sender === undefined ? "sent" : sender}>
        <p className="message-text">{text}</p>
      </div>
    </div>
  );
};

const MessageContainer = props => {
  let messages = props.messageList.map(m => {
    return <Message id={m.id} text={m.text} sender={m.sender} />;
  });
  return <div className="message-container">{messages}</div>;
};

export default MessageContainer;
