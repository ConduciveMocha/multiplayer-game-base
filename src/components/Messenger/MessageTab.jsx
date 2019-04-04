import React from 'react';

const MessageTab = (props) => {
    return(
        <div className="message-tab-container">
            <p className="message-tab-title">{props.title}</p>
            {props.unread ? <div className="unread-message"></div> : null}
        </div>
    )
}


export default MessageTab;