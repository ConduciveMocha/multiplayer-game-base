import React from "react";

const CreateThread = (addedUsers, removeUserFunction) => {
  let addedUserBoxes = addedUsers.map(user => {
    return (
      <li className="added-user-box" key={"addedUserBox." + user.id}>
        <p className="added-username">user.username</p>
        <button className="remove-user" onSubmit={removeUserFunction(user)}>
          "X"
        </button>
      </li>
    );
  });

  return (
    <div className="create-thread-container">
      <ul className="added-users-container">{addedUserBoxes}</ul>
    </div>
  );
};

export default CreateThread;
