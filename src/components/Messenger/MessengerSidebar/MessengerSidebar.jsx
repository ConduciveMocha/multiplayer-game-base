import React from "react";

import CollapsableList from "./CollapsableList";

const UserListItem = ({ item, id }) => {
  return <div key={id}>{item}</div>;
};

const ThreadListItem = thread => {
  return <div />;
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
