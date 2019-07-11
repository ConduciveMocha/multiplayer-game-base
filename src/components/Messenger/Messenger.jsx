import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import MessengerSidebar from "./MessengerSidebar";
import TabContainer from "./TabDisplay/TabContainer";
import MessageContainer from "./TabDisplay/MessageContainer";
import InputContainer from "./TabDisplay/InputContainer";
// ==================================

export const Messenger = props => {
  // Pulls threads, messages from redux state
  const { threads, messages } = useSelector(state => ({
    threads: state.threads,
    messages: state.messages
  }));

  // Thread the user has open
  //! This code only works if there is thread id 0. My intention (7/11/19) is that the global thread
  //! will have id 0. This only works under the assumption that the global thread is loaded before
  //! the messaging componant is mounted. As of right now this breaks the site.
  const [currentThread, setCurrentThread] = useState({
    ...threads[0],
    messages: messages[threads[0].id]
  });

  // Content currently in the input box
  const [inputContent, setInputContent] = useState("");

  // List of the thread ids of the open tabs
  const [openTabIndices, setOpenTabIndices] = useState([0]);

  // Updates openTabIndices with a new tab
  const makeOpenTab = index => () => {
    if (openTabIndices.includes(index)) {
      setCurrentThread({ ...threads[index], messages: messages[index] });
    } else if (threads[index]) {
      setOpenTabIndices(state => [...state, index]);

      setCurrentThread({ ...threads[index], messages: messages[index] });
    } else {
      console.error("Index not associated with thread");
    }
  };

  // Removes index from openTabIndices
  const makeCloseTab = index => () => {
    setOpenTabIndices(state => state.filter(el => el !== index));
  };

  return (
    <div className="messanger-container">
      <MessengerSidebar />
      <div className="tab-display-container">
        <TabContainer />
        <MessageContainer />
        <InputContainer
          inputContent={inputContent}
          onChangeFtn={e => {
            setInputContent(e.target.value);
          }}
        />
      </div>
    </div>
  );
};

export default Messenger;
