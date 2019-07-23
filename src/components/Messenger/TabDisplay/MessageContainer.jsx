import React from "react";

const Message = ({text, sender}) => {
  return (
    <div className="message">
      <div className={sender === 1 ? "sent" : "recieved"}>
        <p className="message-text">{text}</p>
      </div>
    </div>
  );
};
 
const MessageContainer = ({users,messages}) => {
  
  let messageComponants =  messages.map(m => {
    return <Message key={m.id} text={m.content} sender={m.sender} />;
  });
  return <div className="message-container">{messageComponants}</div>;
};

export default MessageContainer;
