import React, { useState, useEffect } from "react";
import { connect } from "react-redux";

import useArray from "../hooks/useArray";
import CreateThread from "./CreateThread";
import Thread from "./Thread";
import Threads from "./Threads";
import UserList from "./UserList";

import {
  sendMessage,
  requestNewThread,
  reportMessageRead
} from "../../actions/message-actions";
//? Switch userslist to a list of available threads?
const Messenger = props => {
  console.log("in messenger props.users is,", props.users);

  // List of open threads. Passed to ThreadTabs so
  // elements can be popped when closed
  const openTabs = useArray([]);

  // Users to add to a new thread
  const newThreadUsers = useArray([]);

  const { showCreateThread, setShowCreateThread } = useState(false);

  return (
    <div className="messenger">
      <UserList users={props.users} userOnClick={user => e => {}} />

      <Threads
        threads={openThreads}
        tabOnClick={thread => e => {
          setActiveThread(thread);
        }}
        tabOnClose={thread => e => {
          openThreads.filter(t => t.id === thread.id);
        }}
      />
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
