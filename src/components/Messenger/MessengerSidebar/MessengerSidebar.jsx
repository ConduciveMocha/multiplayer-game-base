import React from "react";
import ConversationList from "./ConversationList";
import UserList from "./UserList";
export const MessengerSideBar = props => {
  return (
    <div>
      <div className="messenger-sidebar">
        <ConversationList
          threadList={Array.from(props.threadList.values()).sort((th1, th2) =>
            th2 < th1 ? 1 : th1 < th2 ? -1 : 0
          )}
          openThreads={openThreads.value}
          selectThreadItem={thread => e => {
            if (
              !openThreads.value.find(th => thread.threadHash === th.threadHash)
            )
              openThreads.add(thread);
            setActiveThread(thread);
          }}
          clickClose={thread => e => {
            const ind = openThreads.findIndex(
              th => thread.threadHash === th.threadHash
            );
            if (openThreads && ind > -1) openThreads.removeIndex(ind);
            if (thread.threadHash === activeThread.threadHash)
              setActiveThread(
                openThreads.find(th => th.threadHash !== thread.threadHash)
              );
          }}
        />
        <UserList
          friendsList={props.friendsList}
          onlineList={props.onlineList}
          userItemClick={user => e => {
            // Currently adding users to a new thread
            if (activeThread.id === -1) addUserToThread(user);
            // Instead, open thread
            else {
              let members = [user, props.clientUser];
              const thHash = Thread.makeThreadHash(members);
              let existingThread = props.threadMap.get(thHash);

              // Not an existing thread
              if (!existingThread) {
                const newThread = new Thread(-1, "", members, -1);
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
      </div>{" "}
    </div>
  );
};

export default MessengerSideBar;
