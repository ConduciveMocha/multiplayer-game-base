import React, { useState, useEffect } from "react";

const UserList = props => {
  const { searchString, setSearchString } = useState("");

  console.log(searchString);
  // Filters the passed userlist to match the value
  // of the search box, then creates <li> components
  // for the displayed users
  console.log("users", props.users);

  const users = props.users
    .filter(user => {
      if (searchString === "") return true;
      else
        return user.username
          .toLowerCase()
          .startsWith(searchString ? searchString.trim().toLowerCase() : "");
    })
    .map(user => {
      return (
        <li
          className="user"
          key={"user-list" + user.userId}
          onClick={props.userOnClick(user)}
        >
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
