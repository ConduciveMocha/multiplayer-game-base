import React from 'react';


export default ThreadTabs = (props) => {
    return (
        <ul>
            {props.threads.map(el => {
                return (
                    <li className="thread-tab">
                        <p>{el.threadName}</p>
                        <div style={el.hasUnread ? "unread-thread":"thread"}/>
                        <button className="close-thread-button">x</button>
                    </li>
                )
            })}
        </ul>
    )
}