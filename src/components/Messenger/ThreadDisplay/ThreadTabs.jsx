import React from "react";

const Tab = (thread, tabClick, tabClose, isActive) => {
  return (
    <li
      className={isActive ? "thread-tab-active" : "thread-tab-inactive"}
      key={"threadtab." + thread.threadHash}
      onClick={tabClick}
    >
      <p>{thread.threadName}</p>
      <div className={thread.hasUnread ? "tab-unread" : "tab-read"} />
      <button onClick={tabClose} />
    </li>
  );
};

//Needs props:
// --openThreads: [Thread]
// --activeThread: Thread

// -- openGlobalThread: func
// --tabClick: (Thread) => func
// --tabClose: (Thread) => func
// --nav: (Int) => func
export const ThreadTabs = props => {
  const tabList = props.openThreads.map((thread, ind) => {
    const isActive = thread.threadHash === props.activeThread.threadHash;
    return Tab(
      thread.threadName,
      thread.threadHash,
      props.tabClick(thread),
      props.tabClose(thread),
      isActive
    );
  });

  return (
    <div>
      <button
        className="tablist-open-global"
        onClick={e => {
          props.openGlobalThread;
        }}
      />
      <ul>{tablist}</ul>
      <button className="tablist-navigation-left" onClick={props.nav(-1)} />
      <button className="tablist-navigation-right" onClick={props.nav(1)} />
    </div>
  );
};

export default ThreadTabs;
