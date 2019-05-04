import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import useArray from "../../hooks/useArray";
import useCache from "../../hooks/useCache.js";
import ThreadDisplay from "./ThreadDisplay";
import MessengerSidebar from "./MessengerSidebar/Me";

const visibleTabs = (openThreads, shownTabIndex) => {
  const MAX_OPEN_TABS = 8;
};

// TODO: rework the newThreadList so it doesnt actually need to modify the activeThread object
//? threadHash collision bug might be fixed. Needs testing
export const Messenger = props => {
  const openThreads = useArray([props.threadMap.get("0")]);
  const creationThreads = useCache();

  const [activeThread, setActiveThread] = useState(props.threadMap.get("0"));
  const [activeThreadIndex, setActiveThreadIndex] = useState(0);

  // Manages the active thread changing
  useEffect(() => {
    let ind = openThreads.value.findIndex(
      el => el.threadHash === activeThread.threadHash
    );

    // the activeThread has closed
    if (openThreads[ind] === undefined) {
      // a thread replaced the activeThread at activeThread index
      if (openThreads[activeThreadIndex] !== undefined) {
        setActiveThread(openThreads[ind]);
      }
      // Find the next lowest index that is not closed. Garaunteed to hit the global thread
      else {
        do {
          ind--;
          if (openThreads[ind] !== undefined) {
            setActiveThread(openThreads[ind]);
            setActiveThreadIndex(ind);
            return;
          }
        } while (ind > 0);
      }
    } else {
      setActiveThreadIndex(ind);
    }
  }, [openThreads, activeThread]);

  // Manages creationThreads being replaced by realThreads
  useEffect(() => {
    // Thread id hasnt been set ==> pending
    const pendingThreads = openThreads.value.filter(th => th.id === -1);

    // If ther are pending threads
    if (pendingThreads.length !== 0) {
      let upgraded;
      const newOpenThreads = openThreads.value.map(th => {
        if (th.id === -1) {
          upgraded = props.threadMap.get(th.threadHash);
        }
        return upgraded ? upgraded : th;
      });

      openThreads.setValue(newOpenThreads);
    }
  }, [props.threadMap]);

  // TODO: Replace this with a real call
  const sendMessage = (thread, content, style) => {
    console.log("Placeholder for `sendMessage` in `Messenger.jsx`");
  };

  return (
    <div className="messenger-container">
      <MessengerSidebar
        threadList={Array.from(props.threadMap.values)}
        friendsList={props.threadMap.friends}
        onlineList={props.threadMap.online}
      />
      <>
        <TabList
          openThreads={openThreads.value}
          openGlobalThread={() => {} /*setActiveThread(openThreads.value[0])*/}
          activeThread={activeThread}
          tabClick={thread => e => setActiveThread(thread)}
          tabClose={thread => e => {
            openThreads.setValue(arr =>
              arr.filter(th => th && th.threadHash !== thread.threadHash)
            );
          }}
          nav={n => e => {
            console.log(n, e);
          }}
        />

        <ThreadDisplay activeThread={[activeThread, activeThreadIndex]} />
      </>
    </div>
  );
};
export default connect(
  state => {
    return {
      threadMap: state.messaging.threads,
      clientUser: state.login.clientUser,
      userList: state.messaging.users,
      pendingThreads: state.messaging.pendingThreads
    };
  },
  dispatch => {
    return {};
  }
)(Messenger);
