import React from 'react'
const MessageFeed = (props) =>{
    const renderMessage = (message) =>  {
        return (<p>{message}</p>)
    }
    return(
        <div className="message-feed-container">
            {props.messages ? props.messages.map(renderMessage) : null}
        </div>
    )
}
export default MessageFeed;