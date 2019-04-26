import React from "react";

export const ThreadTabList = props => {
  let threadTabList = props.activeThreads.arr.map(el => {
    return (
      <li className="thread-tab">
        <p>{el.threadName}</p>
        <div style={el.hasUnread ? "unread-thread" : "thread"} />
        <button className="close-thread-button">x</button>
      </li>
    );
  });
  return <ul className="thread-tab-list-container">{threadTabList}</ul>;
};

export default ThreadTabList;
