import React from "react";

const shortenThreadName = name => {
  return name.length < 15 ? name : name.slice(0, 12).trim() + "...";
};

const ThreadTab = thread => {
  return (
    <li>
      <div className={thread.hasUnread ? "tab-unread" : "tab-read"} />
      <p>{shortenThreadName(thread.name)}</p>

      {thread.id === 0 ? (
        <div />
      ) : (
        <button className="close-tab-button">x</button>
      )}
    </li>
  );
};

export const TabContainer = props => {
  let tabs = props.threadList.map(th => {
    return <ThreadTab id={th.id} thread={th} />;
  });
  return <div className="tab-container">{tabs}</div>;
};

export default TabContainer;
