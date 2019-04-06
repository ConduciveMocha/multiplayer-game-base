import React from 'react';
const MessageTab = (props) => {
    return(
        <div className={props.thread.active ? "message-tab-active" : "message-tab"}>
            <p className="message-tab-title">{props.thread.threadId}</p>
            {props.thread.unread ? <div className="unread-message">*</div> : null}
        </div>
    )
}


export default MessageTab;