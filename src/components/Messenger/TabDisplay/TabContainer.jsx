import React from "react";
import {
  CREATE_THREAD_ID,
  GLOBAL_THREAD_ID
} from "../../../constants/ThreadIds";
const shortenThreadName = name => {
  return name.length < 15 ? name : name.slice(0, 12).trim() + "...";
};

const ThreadTab = ({ thread, closeThread, focusTab, tabActive }) => {
  return (
    <div
      className={tabActive ? "active-tab" : "tab"}
      onClick={() => focusTab()}
    >
      <div className={thread.hasUnread ? "tab-unread" : "tab-read"} />
      <p
        className={
          thread.id === CREATE_THREAD_ID ? "thread-name-italic" : "thread-name"
        }
      >
        {shortenThreadName(thread.name)}
      </p>

      {
        // Conditional to check if thread is global or not. Messenger Component expects
        // at least one thread to exist at all times, so this prevents the close button
        // to appear for the global thread.
        //! ASSUMES GLOBAL THREAD HAS ID 0!!!!!!!
        <button
          className="close-tab-button"
          disabled={thread.id === GLOBAL_THREAD_ID}
          onClick={() => closeThread()}
        >
          x
        </button>
      }
    </div>
  );
};

export const TabContainer = ({
  threads,
  openTabIds,
  makeCloseTab,
  makeFocusTab,
  currentTabIndex,
  showCreateThread
}) => {
  const tabs = openTabIds
    .map(id => {
      if (id === CREATE_THREAD_ID) {
        return {
          id: CREATE_THREAD_ID,
          name: "New Thread",
          messages: [],
          users: []
        };
      } else {
        return threads[id];
      }
    })
    .map(th => {
      return (
        <ThreadTab
          key={"thread-tab-" + th.id}
          thread={th}
          closeThread={
            th.id !== GLOBAL_THREAD_ID
              ? makeCloseTab(parseInt(th.id))
              : () => {}
          }
          tabActive={openTabIds[currentTabIndex] === th.id}
          focusTab={makeFocusTab(parseInt(th.id))}
        />
      );
    });
  return <div className="tab-container">{tabs}</div>;
};

export default TabContainer;
