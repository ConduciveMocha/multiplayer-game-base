import React, { useState } from "react";

const AddUserItem = (user, removeUser, highlighted, setHighlighted) => {
  <li
    className={highlighted ? "add-user-item-focused" : "add-user-item"}
    key={"AddUserItem." + user.id}
    onClick={setHighlighted}
    onKeyPress={e => {
      if (e.keyCode === 46 && highlighted) removeUser();
    }}
  >
    <p>{user.username}</p>
    <button onClick={removeUser}>X</button>
  </li>;
};

// Needs props
// --removeUser: (User)=>func
// --addedUsers [User]
export const AddUsersBar = props => {
  const [highlightedUser, setHighlightedUser] = useState();
  let addedUsersItems = props.addedUsers.map(user =>
    AddUserItem(
      user,
      props.removeUser(user),
      user.id === highlightedUser.id,
      () => setHighlightedUser(user)
    )
  );

  return <ul className="add-users-bar">{addedUsersItems}</ul>;
};

export default AddUsersBAr;
