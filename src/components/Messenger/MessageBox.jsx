import React, {useState} from 'react'
import {connect} from 'react-redux'
import {messageSent} from '../../actions/message-actions'
const MessageBox = (props) => {
    const [currentText, setCurrentText] = useState('')


    return(
        <div className="message-box-container">
            <textarea
                className="message-box"
                rows="4" cols="33"
                onChange={e=>{setCurrentText(e.target.value)}}
                value={currentText}
                maxLength="128"
            >{currentText}</textarea>
            <button 
                className="send-message-button"
                onClick={e=>{
                        props.handleSend(props.recipientId, currentText, new Date().getTime());
                        setCurrentText('');
                    }
                }
            >Send</button>
        </div>
    )
}
export default connect(
    null,
    dispatch => ({handleSend: (recipientId,content,timestamp) => {dispatch(messageSent(recipientId,content,timestamp))}
   }))(MessageBox);