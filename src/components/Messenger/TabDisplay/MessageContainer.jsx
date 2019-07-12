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

const MessageContainer = messages => {
  let messages = messages.map(m => {
    return <Message key={m.id} text={m.text} sender={m.sender} />;
  });
  return <div className="message-container">{messages}</div>;
};

export default MessageContainer;
