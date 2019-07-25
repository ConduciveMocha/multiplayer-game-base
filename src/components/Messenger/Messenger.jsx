import React, { useState, useEffect,useRef,useCallback} from "react";
import { connect } from "react-redux";
import { sendMessage } from '../../actions/message-actions'
import MessengerSidebar from "./MessengerSidebar";
import TabContainer from "./TabDisplay/TabContainer";
import MessageContainer from "./TabDisplay/MessageContainer";
import InputContainer from "./TabDisplay/InputContainer";
import CreateThread from './CreateThread';
import './Messenger.css'

const useBool = (initial=true) => {
  const [value,setValue] = useState(initial)

  return {
    setTrue: useCallback(()=>setValue(true), []),
    setFalse: useCallback(()=>setValue(false), []),
    toggle: useCallback(()=>setValue(value=>!value),[]),
    setValue,
    value
  }


}



const Messenger = props => {

  
  // Pulls threads, messages from redux state
  const {threads,messages,users} = {threads:props.threads,messages:props.messages, users:props.users}
  
  // List of the thread ids of the open tabs
  const [openTabIds, setOpenTabIds] = useState([0]);
  const [currentTabIndex,setCurrentTabIndex] = useState(0)
  
  // Content currently in the input box
  // Updated on <textarea> change
  const [inputContent, setInputContent] = useState("");
  const [currentMessages, setCurrentMessages] = useState([] )
  
  const [newThreadName, setNewThreadName] = useState("");
  const [addedUsers,setAddedUsers] = useState([1,2,3]);
  const showCreateThread = useBool(true);
  


  const scrollRef = useRef(null)
  // Synchronizes the displayed messages and the currentTabIndex. 
  useEffect(()=>{
    //! DONT TOUCH THIS IF STATEMENT. AVOIDS BUG WHERE currentTabIndex IS OUT OF RANGE
    // If currentTabIndex is out of range, set the open tab to the global thread
    if (currentTabIndex >= openTabIds.length) {
      setCurrentTabIndex(0);
    }
    else{
      const currentThread = threads[openTabIds[currentTabIndex]]
      setCurrentMessages(currentThread.messages.map(id=>{return messages[id]}))
    }
    try{    
      scrollRef.current.scrollTop = Number.MAX_SAFE_INTEGER
    }
    catch (error){
      console.error('Attempt to set scroll position from Messenger useEffect failed')
    }
  }, [messages,currentTabIndex,openTabIds,threads])

  // Creates function to scope to a tab. Used by the thread sidebar list
  const makeFocusTab = id => () => {
    const tabIndex = openTabIds.indexOf(id);
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
    //? Find out where i need to parseInt and where not   
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
  
  const makeRemoveAddedUser = (id) => () => {
    if(addedUsers.indexOf(id) >= 0) {
      const updatedAddedUsers = addedUsers.filter(el => el !== id)
      setAddedUsers(updatedAddedUsers)
    }
    else{
      console.error('There was an attempt to remove a user not found in `addedUsers`')
      console.debug('id', id)
      console.debug('addedUsers',addedUsers)
    }
  }

  const closeCreateThread = () => {
    if(showCreateThread){
      setAddedUsers([]);
      setNewThreadName("")  
      showCreateThread.setFalse();
      setOpenTabIds(openTabs=>openTabs.slice(0,-1)) 
    }
    else{
      console.error('`showCreateThread` is set to false')
    }
  }


  return (
    <div className="messanger-container">
      <MessengerSidebar 
      openTabIds={openTabIds} 
      makeOpenTab={makeOpenTab} 
      makeCloseTab={makeCloseTab}
      makeFocusTab={makeFocusTab} 
      threads={threads}
      users={users} />
      <div className="tab-display-container">
        <TabContainer
          threads={threads}
          makeCloseTab={makeCloseTab}
          makeFocusTab={makeFocusTab}
          currentTabIndex={currentTabIndex}
          openTabIds={openTabIds}
        />
        {showCreateThread.value ? <CreateThread 
                              addedUsers={addedUsers.map(id => users[id])}
                              makeRemoveUser={makeRemoveAddedUser}
                              closeCreateThread={closeCreateThread}
                              /> : 
                              <MessageContainer 
                              users={users} 
                              messages={currentMessages} 
                              scrollRef={scrollRef} 
                              />}
        
        <InputContainer
          inputContent={inputContent}
          onChangeFtn={(e)=>{setInputContent(e.target.value)}}
          sendFtn={()=>{
            props.dispatchMessage(openTabIds[currentTabIndex],inputContent );
            setInputContent("");
          }}
        />
      </div>
      <button onClick={()=>{showCreateThread.toggle()}}>SHOW CREATE THREAD DEBUG</button>
    </div>
  );
};

export default connect(
  state=>({
    messages: state.messaging.messages,
    threads: state.messaging.threads,
    users:state.messaging.users
  }),
  dispatch =>{
    return {
      dispatchMessage: (thread,content) => dispatch(sendMessage(thread,content))
    }
  }
)(Messenger);
