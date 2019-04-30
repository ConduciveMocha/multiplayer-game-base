import React from "react";
import MessageDisplay from "./MessageDisplay";
import MessageInput from "./MessageInput";
import AddUsersBar from "./AddUsersBar";

export const ThreadTabs = props => {
  return (
    <div>
      {activeThread && activeThread.initialized ? (
        ""
      ) : (
        <AddUsersBar
          addedUsers={addedUsersList.value}
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
      <MessageDisplay
        messageList={
          !activeThread
            ? []
            : activeThread.messageList
            ? activeThread.messageList
            : []
        }
      />
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
              if (!openThreads.find(th => officialThreadHash === th.threadHash))
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
  );
};

export default ThreadTabs;
