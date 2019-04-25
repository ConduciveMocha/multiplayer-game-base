import React, { useState } from "react";
import Message from "./Message";
const Thread = props => {
  const [currentMessage, setCurrentMessage] = useState("");

  return (
    <div className="thread-container">
      <div className="thread-display">
        {props.thread.messages.map(el => {
          return <Message messageData={el} />;
        })}
      </div>

      <form className="message-input-container">
        <textarea />
        <div className="message-options-container">
          <input type="checkbox" />
          <input type="checkbox" />
          <input type="color" />
          <input type="range" />
        </div>
        <button
          onSubmit={console.log(
            "If yourre seeing this, add an onSubmit function to the button in Thread.jsx"
          )}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Thread;
