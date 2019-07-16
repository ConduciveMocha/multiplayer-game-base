import React from "react";

const shortenThreadName = name => {
  return name.length < 15 ? name : name.slice(0, 12).trim() + "...";
};

const ThreadTab = ({thread, closeThread, focusTab, tabActive}) => {
  return (
    <div className={tabActive ? "active-tab" : "tab"} onClick={() => focusTab()}>
      <div className={thread.hasUnread ? "tab-unread" : "tab-read"} />
      <p>{shortenThreadName(thread.name)}</p>
      
      { // Conditional to check if thread is global or not. Messenger Component expects
        // at least one thread to exist at all times, so this prevents the close button
        // to appear for the global thread.
        //! ASSUMES GLOBAL THREAD HAS ID 0!!!!!!!
        <button className="close-tab-button" disabled={thread.id===0} onClick={()=> closeThread()}>x</button>
      }
    </div>
  );
};

export const TabContainer = ({threads,openTabIds, makeCloseTab, makeFocusTab,currentTabIndex}) => {
  const tabs = openTabIds.map(id=>{return threads[id]}).map(th => {
    return <ThreadTab 
                key={'thread-tab-'+th.id} 
                thread={th} 
                closeThread={th.id !== 0 ? makeCloseTab(parseInt(th.id)) : ()=>{}}
                tabActive={openTabIds[currentTabIndex] === th.id} 
                focusTab={makeFocusTab(parseInt(th.id))} />;
  });
  return <div className="tab-container">{tabs}</div>;
};

export default TabContainer;
