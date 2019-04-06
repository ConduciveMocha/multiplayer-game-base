import React from 'react'

const Message = (props) => {
    return (
      <div>
        <p>{props.timestamp}</p>
        <p>{props.user}</p> 
        <p>{props.content}</p>
      </div>
    );
}

const MessageFeed = (props) =>{
    const renderMessage = (message) =>  {
        return (<Message key={message.messageId} content={message.content} />)
    }
    return(
        <div className="message-feed-container">
            { props.thread.messages.map(message=>renderMessage(message))}
        </div>
    )
}
export default MessageFeed;