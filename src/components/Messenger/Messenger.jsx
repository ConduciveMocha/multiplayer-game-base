import React, { useState, useEffect } from "react";
import { connect } from "react-redux";

import useArray from "../hooks/useArray";
import CreateThread from "./CreateThread";
import Thread from "./Thread";
import ThreadTabs from "./ThreadTabs";
import UserList from "./UserList";

import {
  sendMessage,
  requestNewThread,
  reportMessageRead
} from "../../actions/message-actions";
//? Switch userslist to a list of available threads?
const Messenger = props => {
  console.log("in messenger props.users is,", props.users);
  const [activeThread, setActiveThread] = useState(null); // Set to a thread object

  // List of open threads. Passed to ThreadTabs so
  // elements can be popped when closed
  const openThreads = useArray([]);

  // Users to add to a new thread
  const newThreadUsers = useArray([]);

  const { showCreateThread, setShowCreateThread } = useState(false);

  return (
    <div className="messenger">
      <ThreadTabs
        threads={openThreads}
        tabOnClick={thread => e => {
          setActiveThread(thread);
        }}
        tabOnClose={thread => e => {
          openThreads.filter(t => t.id === thread.id);
        }}
      />
      <UserList
        users={props.users}
        userOnClick={user => e => {
          // TODO: should open a thread if there is a thread

          // Do this if there isnt a thread
          newThreadUsers.push(user);
          setShowCreateThread(true);
        }}
      />
      {showCreateThread || newThreadUsers.arr ? (
        <CreateThread includeUsers={newThreadUsers.arr} />
      ) : (
        <Thread active={activeThread} />
      )}
    </div>
  );
};

export default connect(
  state => {
    return {
      users: state.messaging.users,
      threads: state.messaging.threads
    };
  },
  dispatch => {
    return {
      sendMessage: message => {
        dispatch(
          sendMessage(
            message.threadId,
            message.content,
            message.fmt,
            message.color
          )
        );
      },
      markAsRead: message => {
        dispatch(reportMessageRead(message.id, message.threadId));
      },
      requestNewThread: (thread, initialMessage) => {
        dispatch(requestNewThread(thread.members, thread.name, initialMessage));
      }
    };
  }
)(Messenger);
