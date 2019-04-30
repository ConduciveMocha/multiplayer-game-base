import React, { useState } from "react";

const UserItem = (user, userItemClick) => {
  return (
    <li key={"user.item." + user.id} onClick={userItemClick(user)}>
      <div className="user-item-img" />
      <p className="user-item-username">{user.username}</p>
      {user.online ? (
        <div className="user-item-online" />
      ) : (
        <div className="user-item-offline" />
      )}
    </li>
  );
};

const UserSubList = props => {
  return (
    <>
      <h4 className="user-sublist-title">{props.sublistName}</h4>
      <ul className="user-sublist-container">
        {props.userList
          ? Array.from(props.userList.values()).map(user =>
              UserItem(user, props.userItemClick)
            )
          : ""}
      </ul>
    </>
  );
};

//Needs Props:
// --onlineList: [User]
// --friendsList: [User]
// --userItemClick: (User) => func
export const UserList = props => {
  const [listOpen, setListOpen] = useState(true);
  return (
    <>
      <div className="sidebar-title">
        <h3>Users</h3>
        <button onClick={e => setListOpen(!listOpen)} />
      </div>

      <div className={listOpen ? "user-list-container" : "user-list-hidden"}>
        <UserSubList
          sublistName="Online"
          userList={props.onlineList}
          userItemClick={props.userItemClick}
        />
        <UserSubList
          sublistName="Friends"
          userList={props.friendsList}
          userItemClick={props.userItemClick}
        />
      </div>
    </>
  );
};

export default UserList;
