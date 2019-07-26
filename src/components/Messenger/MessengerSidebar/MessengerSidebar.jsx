import React from "react";

import CollapsableList from "./CollapsableList";
import useBool from "../../../hooks/useBool";

import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import AddIcon from "@material-ui/icons/Add";
const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1)
  },
  extendedIcon: {
    marginRight: theme.spacing(1)
  }
}));

const UserListItem = ({ user, addThreadUser }) => {
  const optionsOpen = useBool(false);
  // const classes = makeStyles();
  return (
    <div key={user.id}>
      <span
        onClick={() => {
          optionsOpen.toggle();
        }}
      >
        {user.username}
      </span>
      {optionsOpen.value ? (
        <div className="user-list-item-actions">
          <button className="block-user-button" />
          <button className="open-profile-button" />
          <Button
            className={""}
            onClick={() => {
              addThreadUser();
            }}
          >
            <AddIcon />
          </Button>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
};

const ThreadListItem = ({ thread, openTab, closeTab }) => {
  return (
    <div key={"thread-list-item-" + thread.id}>
      <span onClick={() => openTab()}>{thread.name}</span>
      {/* <button disabled={thread.id === 0} onClick={()=>openTab()}>O</button> */}
      <button disabled={thread.id === 0} onClick={() => closeTab()}>
        x
      </button>
    </div>
  );
};

const MessengerSidebar = ({
  openTabIds,
  makeOpenTab,
  makeFocusTab,
  onlineUserIds,
  friendsList,
  makeCloseTab,
  threads,
  users,
  makeAddThreadUser
}) => {
  return (
    <div className={"messenger-sidebar"}>
      <CollapsableList
        ListItemComponent={ThreadListItem}
        proplist={Object.keys(threads).map(id => {
          return {
            thread: threads[id],
            openTab: makeOpenTab(id),
            closeTab: makeCloseTab(id)
          };
        })}
        listName={"Conversations"}
      />

      <hr />

      <CollapsableList
        ListItemComponent={UserListItem}
        proplist={Object.keys(users)
          .filter(el => onlineUserIds.indexOf(parseInt(el)) >= 0)
          .map(id => {
            return {
              user: users[id],
              addThreadUser: makeAddThreadUser(id)
            };
          })}
        listName={"Online Users"}
      />
      <hr />

      <CollapsableList
        ListItemComponent={UserListItem}
        proplist={Object.keys(users)
          .filter(el => friendsList.indexOf(parseInt(el)) >= 0)
          .map(id => {
            return {
              user: users[id],
              addThreadUser: makeAddThreadUser(id)
            };
          })}
        listName={"Friends"}
      />
      <hr />
    </div>
  );
};

export default MessengerSidebar;
