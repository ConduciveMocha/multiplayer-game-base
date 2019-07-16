import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import MessengerSidebar from "./MessengerSidebar";
import TabContainer from "./TabDisplay/TabContainer";
import MessageContainer from "./TabDisplay/MessageContainer";
import InputContainer from "./TabDisplay/InputContainer";

import './Messenger.css'
// ==================================

// const getThreadNames = (threads, threadIds) => {
//   return threadIds.map(id => {
//       return thread[id].name
//   })
// } 


const Messenger = props => {
  // Pulls threads, messages from redux state
  // const { threads, messages,users } = useSelector(state => ({
  //   threads: state.threads,
  //   messages: state.messages,
  //   users: state.users
  // }));
  const {threads,messages,users} = {threads:props.threads,messages:props.messages, users:props.users}

  // List of the thread ids of the open tabs
  const [openTabIds, setOpenTabIds] = useState([0]);
  const [currentTabIndex,setCurrentTabIndex] = useState(0)
  
    // Content currently in the input box
    // Updated on <textarea> change
  const [inputContent, setInputContent] = useState("");
  const [currentMessages, setCurrentMessages] = useState([] )
  
  useEffect(()=>{
    if (currentTabIndex >= openTabIds.length) {
      setCurrentTabIndex(0);
    }
    else{
      const currentThread = threads[openTabIds[currentTabIndex]]
      console.log('in effect',threads,openTabIds,currentTabIndex,currentThread)
      setCurrentMessages(currentThread.messages.map(id=>{return messages[id]}))
    }
  }, [messages,currentTabIndex,openTabIds,threads])

  //! Yes I mean to use id here. Read the code dummy
  const makeFocusTab = id => () => {
    const tabIndex = openTabIds.indexOf(id);
    console.log(tabIndex)
    if (tabIndex < 0) {
      console.error('Tab Id not found: ', id)
    }
    else{
      setCurrentTabIndex(tabIndex);
    }
  }

  // Updates openTabIndices with a new tab
  const makeOpenTab = id => () => {
    if (openTabIds.indexOf(parseInt(id)) < 0) {
      setCurrentTabIndex(openTabIds.length)
      setOpenTabIds([...openTabIds, parseInt(id)])
    }
    else{
      setCurrentTabIndex(openTabIds.indexOf(parseInt(id)))
    }
  
  }
    const makeCloseTab = id => () =>{
      
      const closedTabIndex = openTabIds.indexOf(parseInt(id));

      // Controls what tab will appear when the current tab is closed
      // Attempts to mimic chromes tab closing behavior
      if(closedTabIndex < 0 ) {
        console.error('Tab Id not found: ', id);
      }
      else if (closedTabIndex === 0) {
        console.error('Trying to close the global thread. Youre not supposed to be able to do this...')
      }
      else if (closedTabIndex < currentTabIndex) {
        setCurrentTabIndex(currentTabIndex - 1)
        console.log('closedTabIndex<currentTabIndex',currentTabIndex - 1)
      }
      // Closing currently active tab pulls up the global thread.
      else if (closedTabIndex === currentTabIndex)  {
        setCurrentTabIndex(currentTabIndex*0)
        console.log('closedTabIndex===currentTabIndex', 0)
      }
      setOpenTabIds(openTabIds.filter(el=>el !== parseInt(id)))

     }
    
     console.log('completely fucky statement',openTabIds,currentTabIndex,openTabIds[currentTabIndex],threads[openTabIds[currentTabIndex]] )

  return (
    <div className="messanger-container">
    <p>{currentTabIndex}</p>
      <MessengerSidebar 
      openTabIds={openTabIds} 
      makeOpenTab={makeOpenTab} 
      makeCloseTab={makeCloseTab}
      makeFocusTab={makeFocusTab} 
      threads={props.threads}
      users={props.users} />
      <div className="tab-display-container">
        <TabContainer
          threads={threads}
          makeCloseTab={makeCloseTab}
          makeFocusTab={makeFocusTab}
          currentTabIndex={currentTabIndex}
          openTabIds={openTabIds}
        />
        <MessageContainer users={users} messages={currentMessages} />
        <InputContainer
          inputContent={inputContent}
          onChangeFtn={(e)=>{setInputContent(e.target.value)}}
          sendFtn={props.sendMessage}
        />
      </div>
    </div>
  );
};
export default Messenger;
// export default connect(
//   state=>(
//   {
//     messages: state.messages,
//     threads: state.threads,
//     users:state.users
//   }  
//   ),
//   dispatch =>{
//     return{
//       sendMessage: (msg) => dispatch({type:'MESSAGE_SENT', message:msg})
//     }
//   }

// )(Messenger);
