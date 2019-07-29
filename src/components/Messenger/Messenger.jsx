import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import {
  sendMessage,
  requestNewThread,
  clearNewThread
} from "../../actions/message-actions";
import MessengerSidebar from "./MessengerSidebar";
import TabContainer from "./TabDisplay/TabContainer";
import MessageContainer from "./TabDisplay/MessageContainer";
import InputContainer from "./TabDisplay/InputContainer";
import CreateThread from "./CreateThread";
import useBool from "../../hooks/useBool";
import { CREATE_THREAD_ID } from "../../constants/ThreadIds";
import "./Messenger.css";

const Messenger = props => {
  // Renames redux state variables so i dont have to write props.* everywhere
  const { threads, messages, users, onlineUserIds, friendsList } = {
    threads: props.threads,
    messages: props.messages,
    users: props.users,
    onlineUserIds: props.onlineUserIds,
    friendsList: props.friendsList,
    newThreadId: props.newThreadId
  };

  /*State variables for message views*/
  // List of the thread ids of the open tabs
  const [openTabIds, setOpenTabIds] = useState([0]);
  const [currentTabIndex, setCurrentTabIndex] = useState(0);
  const [inputContent, setInputContent] = useState("");
  const [currentMessages, setCurrentMessages] = useState([]);

  /*State variables for create thread views*/
  const [newThreadName, setNewThreadName] = useState("");
  const [addedUsers, setAddedUsers] = useState([]);
  const showCreateThread = useBool(false);

  // Synchronizes the displayed messages and the currentTabIndex.
  useEffect(() => {
    //! DONT TOUCH THIS IF STATEMENT. AVOIDS BUG WHERE currentTabIndex IS OUT OF RANGE
    // If currentTabIndex is out of range, set the open tab to the global thread
    if (currentTabIndex >= openTabIds.length) {
      setCurrentTabIndex(0);
    } else {
      const currentThread = threads[openTabIds[currentTabIndex]];
      if (currentThread) {
        setCurrentMessages(
          currentThread.messages.map(id => {
            return messages[id];
          })
        );
        showCreateThread.setFalse();
      } else {
        setCurrentMessages([]);
        showCreateThread.setTrue();
      }
    }
  }, [messages, currentTabIndex, openTabIds, threads, showCreateThread.value]);

  useEffect(() => {
    console.log("In effect: ", openTabIds);

    const createThreadIndex = openTabIds.indexOf(CREATE_THREAD_ID);
    if (createThreadIndex < 0) {
      console.log(createThreadIndex);
      console.error("createThread not found in list");
    } else {
      let updatedOpenTabIds = openTabIds.slice();
      updatedOpenTabIds[createThreadIndex] = props.newThreadId;
      setOpenTabIds(updatedOpenTabIds);
      showCreateThread.setFalse();
      props.dispatchClearNewThread();
    }
  }, [props.newThreadId]);

  // Creates function to scope to a tab. Used by the thread sidebar list
  const makeFocusTab = id => () => {
    if (id === CREATE_THREAD_ID) {
      console.debug("Making a focusTab for createThread");
      showCreateThread.setTrue();
    } else {
      showCreateThread.setFalse();
    }
    const tabIndex = openTabIds.indexOf(id);
    if (tabIndex < 0) {
      console.error("Tab Id not found: ", id);
    } else {
      setCurrentTabIndex(tabIndex);
    }
  };

  // Updates openTabIndices with a new tab
  const makeOpenTab = id => () => {
    if (openTabIds.indexOf(parseInt(id)) < 0) {
      setCurrentTabIndex(openTabIds.length);
      setOpenTabIds([...openTabIds, parseInt(id)]);
    } else {
      setCurrentTabIndex(openTabIds.indexOf(parseInt(id)));
    }
    if (id === CREATE_THREAD_ID) {
      showCreateThread.setTrue();
    } else {
      showCreateThread.setFalse();
    }
  };
  const makeCloseTab = id => () => {
    //? Find out where i need to parseInt and where not
    const closedTabIndex = openTabIds.indexOf(parseInt(id));

    // Controls what tab will appear when the current tab is closed
    // Attempts to mimic chromes tab closing behavior

    // Case if the open tab is a newly created tab
    if (parseInt(id) === CREATE_THREAD_ID) {
      console.log("Closing create thread");
      setNewThreadName("");
      setAddedUsers([]);
      showCreateThread.setFalse();
      setCurrentTabIndex(0);
    }
    // Id not found
    else if (closedTabIndex < 0) {
      console.error("Tab Id not found: ", id);
    }
    // Attempted to close the global thread
    else if (closedTabIndex === 0) {
      console.error(
        "Trying to close the global thread. Youre not supposed to be able to do this..."
      );
    }
    // Thread id closed is some id before current id
    else if (closedTabIndex < currentTabIndex) {
      setCurrentTabIndex(currentTabIndex - 1);
      console.log("closedTabIndex<currentTabIndex", currentTabIndex - 1);
    }
    // Closing currently active tab pulls up the global thread.
    else if (closedTabIndex === currentTabIndex) {
      setCurrentTabIndex(0);
      console.log("closedTabIndex===currentTabIndex", 0);
    }
    // Remove thread from openTabIds
    setOpenTabIds(openTabIds.filter(el => el !== parseInt(id)));
  };

  const closeCreateThread = () => {
    if (showCreateThread.value) {
      setAddedUsers([]);
      setNewThreadName("");
      showCreateThread.setFalse();
      setOpenTabIds(openTabs => openTabs.slice(0, -1));
    } else {
      console.error("`showCreateThread` is set to false");
    }
  };

  const makeRemoveThreadUser = id => () => {
    if (addedUsers.indexOf(id) >= 0) {
      const updatedAddedUsers = addedUsers.filter(el => el !== id);
      setAddedUsers(updatedAddedUsers);

      // Close window if no users remain
      //? Maybe rethink this behavior
      if (updatedAddedUsers.length === 0) {
        closeCreateThread();
      }
    } else {
      console.error(
        "There was an attempt to remove a user not found in `addedUsers`"
      );
      console.debug("id", id);
      console.debug("addedUsers", addedUsers);
    }
  };

  const makeAddThreadUser = id => () => {
    id = parseInt(id);
    if (addedUsers.length === 0) {
      console.log("Making a createThread tab", id);
      setAddedUsers([id]);
      setNewThreadName("");
      showCreateThread.setTrue();
      // setCurrentTabIndex(openTabIds.length);
      setOpenTabIds(openids => [...openTabIds, -1]);
      setCurrentTabIndex(openTabIds.length);
    } else if (addedUsers.indexOf(id) < 0) {
      setAddedUsers([...addedUsers, id]);
    } else {
      console.debug("User already added");
      console.debug("`addedUsers`", addedUsers);
      console.debug("`id`", id);
    }
  };

  const onNameChange = e => {
    if (e.target.value.length < 33) setNewThreadName(e.target.value);
    else {
      console.log("Name cant exceed 32 characters ");
      console.debug("Attempted to set to:", e.target.value);
    }
  };
  const sendMessage = e => {
    if (!showCreateThread.value) {
      props.dispatchMessage(openTabIds[currentTabIndex], inputContent);
      setInputContent("");
    } else {
      console.error(
        "Attempt to send message to thread while create thread screen was visible"
      );
      console.debug("openTabIds", openTabIds);
      console.debug("currentTabIndex", currentTabIndex);
      console.debug("showCreateThread", showCreateThread);
    }
  };
  const sendNewThreadRequest = e => {
    if (!showCreateThread.value) {
      console.error(
        "Attempt to request thread while createThread screen not visible."
      );
      console.debug("openTabIds", openTabIds);
      console.debug("currentTabIndex", currentTabIndex);
      console.debug("showCreateThread", showCreateThread);
    } else if (openTabIds[currentTabIndex] !== CREATE_THREAD_ID) {
      console.error("Attempt to request thread from existing thread");
      console.debug("openTabIds", openTabIds);
      console.debug("currentTabIndex", currentTabIndex);
      console.debug("showCreateThread", showCreateThread);
    } else {
      //! Sender set to default value
      props.dispatchRequestNewThread(
        0,
        addedUsers,
        newThreadName,
        inputContent
      );
      setInputContent("");
      setNewThreadName("");
      setAddedUsers([]);
      showCreateThread.setFalse();
    }
  };

  return (
    <div className="messanger-container">
      <MessengerSidebar
        openTabIds={openTabIds}
        makeOpenTab={makeOpenTab}
        makeCloseTab={makeCloseTab}
        makeFocusTab={makeFocusTab}
        threads={threads}
        users={users}
        makeAddThreadUser={makeAddThreadUser}
        onlineUserIds={onlineUserIds}
        friendsList={friendsList}
      />
      <div className="tab-display-container">
        <TabContainer
          threads={threads}
          makeCloseTab={makeCloseTab}
          makeFocusTab={makeFocusTab}
          currentTabIndex={currentTabIndex}
          openTabIds={openTabIds}
          showCreateThread={showCreateThread.value}
        />
        {showCreateThread.value ? (
          <CreateThread
            newThreadName={newThreadName}
            onNameChange={onNameChange}
            addedUsers={addedUsers.map(id => users[id])}
            makeRemoveUser={makeRemoveThreadUser}
            closeCreateThread={closeCreateThread}
          />
        ) : (
          <MessageContainer users={users} messages={currentMessages} />
        )}

        <InputContainer
          inputContent={inputContent}
          onChangeFtn={e => {
            setInputContent(e.target.value);
          }}
          sendFtn={showCreateThread.value ? sendNewThreadRequest : sendMessage}
        />
      </div>
    </div>
  );
};

export default connect(
  state => ({
    messages: state.messaging.messages,
    threads: state.messaging.threads,
    users: state.messaging.users,
    onlineUserIds: state.messaging.onlineUserIds,
    friendsList: state.messaging.friendsList,
    newThreadId: state.messaging.newThreadId
  }),
  dispatch => {
    return {
      dispatchMessage: (thread, content) =>
        dispatch(sendMessage(thread, content)),
      dispatchRequestNewThread: (sender, users, threadName, content) =>
        dispatch(requestNewThread(sender, users, threadName, content)),
      dispatchClearNewThread: () => dispatch(clearNewThread())
    };
  }
)(Messenger);
