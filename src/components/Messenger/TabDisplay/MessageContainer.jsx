import React from "react";

const Message = ({ text, sender }) => {
  return (
    <div className="message">
      <div className={sender === 1 ? "sent" : "recieved"}>
        <p className="message-text">{text}</p>
      </div>
    </div>
  );
};

const MessageContainer = ({ users, messages }) => {
  console.log('Messages',messages)
  let messageComponants = messages.map(m => {
    console.log('Rendering Message:',m)
    return <Message key={m.id} text={m.content} sender={m.sender} />;
  });
  return <div className="message-container">{messageComponants}</div>;
};

export default MessageContainer;
