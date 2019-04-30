import React from "react";
const TabListItem = (thread, tabClick, tabClose, isActive) => {
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
export const TabList = props => {
  console.log(props.openThreads);
  const tabList = props.openThreads
    ? props.openThreads.map((thread, ind) => {
        console.log(thread);
        const isActive =
          props.activeThread &&
          thread.threadHash === props.activeThread.threadHash;
        return TabListItem(
          thread,
          props.tabClick(thread),
          props.tabClose(thread),
          isActive
        );
      })
    : [];

  return (
    <div>
      <button
        className="tablist-open-global"
        onClick={e => {
          props.openGlobalThread();
        }}
      />
      <ul>{tabList}</ul>
      <button className="tablist-navigation-left" onClick={props.nav(-1)} />
      <button className="tablist-navigation-right" onClick={props.nav(1)} />
    </div>
  );
};
