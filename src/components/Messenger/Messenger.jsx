import React,{useState, useRef} from 'react'
import MessageTab from './MessageTab'
import MessageBox from './MessageBox'
import MessageFeed from './MessageFeed'
import UserList from './UserList'
import {connect} from 'react-redux'


import './Messenger.css'
const Messenger = (props) => {
    const [openThreads, setOpenThreads] = useState([]);
    const [currentThread,setCurrentThread] = useState({});
    const [savedInputs, setSavedInputs] = useState({})
    const threadTabs = openThreads.map(th => {
        return (<MessageTab 
                    key={th.threadId}
                    isCurrent={th.threadId === currentThread.threadId} 
                    thread={th} 
                    onTabFocus={e=>{setCurrentThread(th)}}
                />)
    });


    const openThread = userId => e => {
                
    }

    return(
        <div className="messenger-container">
            <div className="tab-container">
                {threadTabs}
            </div>
            <UserList users={props.users} createOnClick={openThread}/>
            <MessageFeed thread={currentThread}/>
            <MessageBox 
                currentText={savedInputs[currentThread.threadId]} 
                onChangeFunction={s=>{
                    let newSavedInputs = {...savedInputs};
                    newSavedInputs[currentThread.threadId] = s;
                    setSavedInputs(newSavedInputs);
                }}
            />
        </div>
    )
}
// export default  connect(
//     state => {
//         return {
//             activeThreads: state.messaging.activeThreads,
//             currentThread: state.messaging.currentThread,
//             users: state.messaging.users
//         }
//     },
//     null
// )(Messenger);
export default Messenger;