import React from 'react';

const Message = (props) => {
    return (
        <div className="message-container">
            <p className="message-text" style={props.message.style}>{props.messaage.content}</p>
        </div>
    )
}

export default Message;