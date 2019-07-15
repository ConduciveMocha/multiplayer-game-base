import React from "react";

const shortenThreadName = name => {
  return name.length < 15 ? name : name.slice(0, 12).trim() + "...";
};

const ThreadTab = ({thread, closeThread, focusTab}) => {
  return (
    <li onClick={() => focusTab()}>
      <div className={thread.hasUnread ? "tab-unread" : "tab-read"} />
      <p>{shortenThreadName(thread.name)}</p>
      
      { // Conditional to check if thread is global or not. Messenger Component expects
        // at least one thread to exist at all times, so this prevents the close button
        // to appear for the global thread.
        //! ASSUMES GLOBAL THREAD HAS ID 0!!!!!!!
        thread.id === 0 ? (
        <div />
      ) : (
        <button className="close-tab-button" onClick={()=> closeThread()}>x</button>
      )}
    </li>
  );
};

export const TabContainer = ({threads,openTabIds, makeCloseTab, makeFocusTab}) => {
  let tabs = openTabIds.map(id=>{return threads[id]}).map(th => {
    return <ThreadTab 
                key={th.id} 
                thread={th} 
                closeThread={makeCloseTab(th)} 
                focusTab={makeFocusTab(th)} />;
  });
  return <div className="tab-container">{tabs}</div>;
};

export default TabContainer;
