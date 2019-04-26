import React, { useState, useEffect } from "react";
import useArray from "../../hooks/useArray";

import UserList from "./Sidebar/UserList";
import ConversationList from "./Sidebar/ConversationList";
import ThreadTabs from "./ThreadDisplay/ThreadTabs";
import MessageDisplay from "./ThreadDisplay/MessageDisplay";
import MessageInput from "./ThreadDisplay/MessageInput";
import AddUsersBar from "./ThreadDisplay/AddUsersBar";

import Thread from "../../api/models/thread";
import Message from "../../api/models/message";

//Conversation List Needs props:
// -threadList: [Threads]  --ADDED
// -openThreads: [Threads] --ADDED
// -selectThreadItem: (thread) => func --ADDED
// -clickClose: (thread) => func --ADDED
//
//UserList Needs Props:
// --onlineList: [User] --ADDED
// --friendsList: [User] --ADDED
// --userItemClick: (User) => func --BUGS
//
// ThreadTabs: Needs props:
// --openThreads: [Thread] -- ADDED
// --activeThread: Thread -- ADDED
// -- openGlobal: func  --ADDED
// --tabClick: (Thread) => func --ADDED
// --tabClose: (Thread) => func --ADDED
//
// AddUsersBar Needs props
// --removeUser: (User)=>func --ADDED
// --addedUsers [User] --ADDED
//
// MessageDisplay Needs Props:
// -messageList: [message] --ADDED
//
// MesseageInput needs props:
// --sendMessage: func(content,style)

// TODO: Theres a bug with how im handling the threadHash of new threads. There can be collisions with existing threads
export const Messenger = props => {
  const openThreads = useArray([]);
  const [activeThread, setActiveThread] = useState();
  const addedUsersList = useArray([]);

  const addUserToThread = user => {
    addedUsersList.add(user);
    const newActive = { ...activeThread };
    newActive.setMembers(addedUsersList.value);
    openThreads.setValue(
      ...openThreads.value.filter(
        th => th.threadHash !== activeThread.threadHash
      ),
      newActive
    );
    setActiveThread(newActive);
  };
  // TODO: Replace this with a real call
  const sendMessage = (thread, content, style) => {
    console.log("Placeholder for `sendMessage` in `Messenger.jsx`");
  };
  useEffect(() => {
    const pendingThreads = openThreads.value.filter(th => th.id === -1);
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

  return (
    <div className="messenger-container">
      <div className="messenger-sidebar">
        <ConversationList
          threadList={props.threadMap
            .values()
            .sort((th1, th2) => (th2 < th1 ? 1 : th1 < th2 ? -1 : 0))}
          openThreads={openThreads.value}
          selectThreadItem={thread => e => {
            if (!openThreads.find(th => thread.threadHash === th.threadHash))
              openThreads.add(thread);
            setActiveThread(thread);
          }}
          clickClose={thread => e => {
            const ind = openThreads.findIndex(
              th => thread.threadHash === th.threadHash
            );

            if (ind > -1) openThreads.removeIndex(ind);

            if (thread.threadHash === activeThread.threadHash)
              setActiveThread(
                openThreads.find(th => th.threadHash !== thread.threadHash)
              );
          }}
        />
        <UserList
          friendsList={props.userList.friends}
          onlineList={props.userList.online}
          userItemClick={user => e => {
            // Currently adding users to a new thread
            if (activeThread.id === -1) addUserToThread(user);
            // Instead, open thread
            else {
              let members = [user, clientUser];
              const thHash = Thread.makeThreadHash(members);
              let existingThread = props.threadMap.get(thHash);

              // Not an existing thread
              if (!existingThread) {
                const newThread = Thread(-1, "_" + thHash, "", members, -1);
                addedUsersList.add(user);
                openThreads.add(newThread);
                setActiveThread(newThread);
              }
              // Open and existing thread
              else {
                // Existing but not open
                if (openThreads.value.find(th => th.threadHash === thHash))
                  setActiveThread(existingThread);
                openThreads.add(existingThread);
              }
            }
          }}
        />
      </div>
      <div>
        <ThreadTabs
          openThreads={openThreads}
          openGlobalThread={setActiveThread(openThreads.value[0])}
          activeThread={activeThread}
          tabClick={thread => e => setActiveThread(thread)}
          tabClose={thread => e => {
            openThreads.setValue(arr =>
              arr.filter(th => th && th.threadHash !== thread.threadHash)
            );
          }}
        />
        {activeThread.initialized ? (
          ""
        ) : (
          <AddUsersBar
            addedUsers={addedUsersList}
            removeUser={user => e => {
              const newAddedUsersList = addedUsersList.value.filter(
                addedUser => user.id !== addedUser.id
              );
              addedUsersList.setValue(newAddedUsersList);
              if (newAddedUsersList.length === 0) {
                const newActive = openThreads.find(
                  th => th.threadHash !== activeThread.threadHash
                );
                activeThread.setActiveThread(newActive);
              }
            }}
          />
        )}
        <MessageDisplay messageList={activeThread.messageList} />
        <MessageInput
          onSendMessage={(content, style) => {
            // First message of a new Thread
            if (activeThread.threadHash[0] === "_") {
              // Get existing thread object
              const officialThreadHash = activeThread.threadHash.slice(1);
              const existingThread = props.threadMap.get(officialThreadHash);

              // Thread already exists
              if (existingThread) {
                // Existing thread is not open
                if (
                  !openThreads.find(th => officialThreadHash === th.threadHash)
                )
                  openThreads.add(existingThread);
                sendMessage(existingThread, content, style);
                setActiveThread(existingThread);
              }
              // Create a message with the uninitialized thread
              else {
                sendMessage(activeThread, content, style);
                setActiveThread({
                  ...activeThread,
                  initialized: true,
                  threadHash: officialThreadHash
                });
              }

              // Remove creation thread
              openThreads.setValue(arr =>
                arr.filter(th => th.threadHash !== officialThreadHash)
              );
            }
            // Existing thread
            else {
              sendMessage(activeThread, content, style);
            }
          }}
        />
      </div>
    </div>
  );
};

export default Messenger;
