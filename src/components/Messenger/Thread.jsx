import React, {useState} from 'react';
import Message from './Message';
const Thread = (props) => {
    const [currentMessage, setCurrentMessage] = useState("");
    
    return (
      <div className="thread-container">
        <div className="thread-display">
            {
                props.thread.messages.map(el => {
                    <Message messageData={el} />;
                })
            }
        </div>

        <form className="message-input-container">
            <textarea />
            <div className="message-options-container">
                <input type="checkbox"/>
                <input type="checkbox"/>
                <input type="color"/>
                <input type="range"/>
            </div>          
            <button>Send</button>        
        </form>
      </div>
    );
}

export default Thread;