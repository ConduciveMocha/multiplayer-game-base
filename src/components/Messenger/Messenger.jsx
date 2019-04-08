import React, {useState, useEffect} from 'react';
import useArray from '../hooks/useArray';

const Messenger = (props) => {
    const [activeThread,setActiveThread] = useState(null); // Set to a thread object
    const openThreads = useArray([]); // threads that are open in the user's window
    
    // Serves two purposes:
    // 1. If array is empty, that will cause a thread to render as opposed to the 
    //    create thread window.
    // 2. Stores a list of users to add to the new thread.
    const createNewThread = useArray([]); 

    // Effect that handles the active thread being closed
    useEffect(()=>{
        if (!openThreads.arr.find(el=>activeThread.threadId === el.threadId)) {
            if(openThreads.arr) setActiveThread(openThreads.arr[0]);
            else setActiveThread(null);
        }
    }, [openThreads])



    return (
        <div className="messenger">
            <ThreadTabs threads={openThreads} />
            <UserList users={props.users} onClickFunction={user => e => { createNewThread.push(user) }}/>
            {createNewThread ? <CreateThread 
                    includeUsers={createNewThread.arr} 
                    /> : <Thread active={activeThread} />}
        </div>
    )
}
