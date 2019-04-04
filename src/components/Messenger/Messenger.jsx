import React,{useState} from 'react'
import MessageTab from './MessageTab'
import MessageBox from './MessageBox'
import MessageFeed from './MessageFeed'
import {connect} from 'react-redux'
import './Messenger.css'
const Messenger = (props) => {
    const [currentTab, setCurrentTab] = useState("0")
    const [currentConversations, setCurrentConversations] = useState(["0"])
    const [unreadList, setUnreadList] = useState({"0":false})
    return(
        <div className="messenger-container">
            <div className="tab-container">
                {/* {
                    props.threads.map((con) => (
                        <MessageTab unread={unreadList[con]} title={props.users[con]}/>
                    )
                )} */}
            </div>
            <MessageFeed messages={props.threads[currentTab]}/>
            <MessageBox/>

        </div>
    )
}
export default  connect(
    state => {
        return {
            threads: state.messaging.threads,
            lastSent: state.messaging.lastSent,
            users: state.messaging.users
        }
    },
    null
)(Messenger);