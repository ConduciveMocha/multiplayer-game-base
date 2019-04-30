import React, { useState } from "react";

const ThreadItem = (thread, isOpen, selectThreadItem, clickClose) => {
  return (
    <li
      className="thread-item"
      key={"thread.item." + thread.threadHash}
      onClick={selectThreadItem}
    >
      <p className="thread-item-name">{thread.threadName}</p>
      {isOpen ? (
        <div className="thread-item-open">
          <button onSubmit={clickClose} />
        </div>
      ) : (
        <div className="thread-item-closed" />
      )}
    </li>
  );
};

// Needs props:
// -threadList: [Threads]
// -openThreads: [Threads]
// -selectThreadItem: (thread) => func
// -clickClose: (thread) => func
export const ConversationList = props => {
  const [listOpened, setListOpened] = useState(true);

  let threadItems = props.threadList.map(thread => {
    let isOpen = props.openThreads.some(
      th => th.threadHash === thread.threadHash
    );
    return ThreadItem(
      thread,
      isOpen,
      props.selectThreadItem(thread),
      props.clickClose(thread)
    );
  });

  return (
    <>
      <div className="sidebar-title">
        <h3>Conversations</h3>
        <button onClick={e => setListOpened(!listOpened)} />
      </div>
      <ul
        className={
          listOpened
            ? "conversation-list-container"
            : "conversation-list-hidden"
        }
      >
        {threadItems}
      </ul>
    </>
  );
};

export default ConversationList;
