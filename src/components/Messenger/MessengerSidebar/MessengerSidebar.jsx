import React from "react";

import CollapsableList from "./CollapsableList";

const UserListItem = ({ user, createNewThread }) => {
  return <div key={user.id} onClick={e => createNewThread()} />;
};

const ThreadListItem = ({ thread, openTab, closeTab }) => {
  <div
    key={thread.id}
    onClick={() => {
      openTab();
    }}
  >
    <span>{thread.name}</span>
    <button onClick={() => closeTab()}>x</button>
  </div>;
};

const MessengerSidebar = props => {
  return (
    <div>
      <CollapsableList
        ListItemComponent={ThreadListItem}
        proplist={[]}
        listName={"Conversations"}
      />
      <CollapsableList
        ListItemComponent={UserListItem}
        proplist={[
          { item: "a", id: 1 },
          { item: "b", id: 2 },
          { item: "c", id: 3 }
        ]}
        listName={"Online Users"}
      />

      <CollapsableList
        ListItemComponent={UserListItem}
        proplist={[]}
        listName={"Friends"}
      />
    </div>
  );
};

export default MessengerSidebar;
