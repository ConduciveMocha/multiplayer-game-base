import React, { useState } from "react";

export const UserList = (userList, onClickFunction) => {
  const { searchString, setSearchString } = useState("");

  // Filters the passed userlist to match the value
  // of the search box, then creates <li> components
  // for the displayed users

  const users = userList
    .filter(user => {
      if (searchString === "") return true;
      else
        return user.username
          .toLowerCase()
          .startsWith(searchString.trim().toLowerCase());
    })
    .map(user => {
      return (
        <li className="user" key={user.userId} onClick={onClickFunction(user)}>
          <div className="user-avatar" />
          <p className="user-username">{user.username}</p>
          <div
            className={
              user.online ? "user-status-online" : "user-status-offline"
            }
          />
        </li>
      );
    });

  return (
    <div className="userlist-contatiner">
      <input
        className="userlist-search"
        type="text"
        onChange={e => {
          setSearchString(e.target.value);
        }}
      />
      <ul className="userlist">{users}</ul>
    </div>
  );
};

export default UserList;
