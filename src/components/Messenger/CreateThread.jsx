import React from "react";

const AddedUser = ({ username, removeUser, focused }) => {
  return (
    <div className={focused ? "added-user-focused" : "added-user"}>
      <span>{username}</span>
      <button onClick={() => removeUser()}>x</button>
    </div>
  );
};

const CreateThread = ({ addedUsers, makeRemoveUser, closeCreateThread,onNameChange }) => {
  const addedUserList = addedUsers.map(user => (
    <AddedUser
      username={user.username}
      makeRemoveUser={user.id}
      focused={false}
      key={"addedUser-" + user.id}
      removeUser={makeRemoveUser(user.id)}
    />
  ));
    
  return (
    <div className="create-thread-container">
      <div>
        <input type="text"  onChange={(e)=>onNameChange(e)}/>
        <button onClick={() => closeCreateThread()}>x</button>
      </div>
      <div className="added-users-container">{addedUserList}</div>
    </div>
  );
};

export default CreateThread;
