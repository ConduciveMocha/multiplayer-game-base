import React from "react";

import CollapsableList from "./CollapsableList";

const UserListItem = ({ user, createNewThread }) => {
  return (
  <div key={user.id} onClick={e => createNewThread()} >
    <span>{user.username}</span>
    <button className="block-user-button"></button>
    <button className="open-profile-button"></button>
  </div>
  );
};

const ThreadListItem = ({ thread, openTab, closeTab }) => {
  return (
    <div
      key={"thread-list-item-" + thread.id}
    >
      <span>{thread.name}</span>
      <button onClick={()=>openTab()}>O</button>
      <button onClick={() => closeTab()}>x</button>
    </div>
  );
};

const MessengerSidebar = ({openTabIds, makeOpenTab,makeFocusTab, makeCloseTab,threads,users}) => {
  return (
    <div>
      <CollapsableList
        ListItemComponent={ThreadListItem}
        proplist={Object.keys(threads).map(id=> {
          console.log(id);
          return {thread:threads[id], openTab:makeOpenTab(id), closeTab:makeCloseTab(id)}
        })}
        listName={"Conversations"}
      />
      {/* <CollapsableList
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
      /> */}
    </div>
  );
};

export default MessengerSidebar;
