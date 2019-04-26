import React, { useState } from "react";
import {connect} from 'react-redux'

import {StyleEnum,textStyles,colorFromInt} from '../../../utils/text-styling'

const ColorPicker = (setColor) => {
    const N_COLORS = 8;

    let = colorOptions = [...Array(N_COLORS).keys()].map(ind=> {
        const colorString  = colorFromInt(ind,N_COLORS)
        return (<option value={colorString} style={{ color: colorString }} key={'colorpicker.' + colorString}>■</option>)
    })
    return(
        <select className='text-color-picker' onChange={e=>setColor(e.target.value)}>
            {colorOptions}
        </select>
    )
}


// Needs props:
// --onSendMessage: func(content,style)
const MessageInput = props => {
    MAX_CHARS=255;
    const [content, setContent] = useState([""]);
    const [style, setStyle] = useState({...textStyles(0),color:'#000'});

    const styleButton = styleType => () =>
        setStyle({...style, text:StyleEnum.toggleStyle(style, styleType)});
    return (
        <div>
            < div className="input-container">
                <textarea
                    className="message-text-input"
                    rows={4}
                    cols={60}
                    style={style}
                    onInput={e => {
                        if (e.target.value<MAX_CHARS)
                            setContent(e.target.value);
                        else 
                            e.target.value = content;
                    }}
                />
            </div>
            <div>
                <button className="toggle-bold" onClick={styleButton(StyleEnum.BOLD)} />
                <button className="toggle-italic" onClick={styleButton(StyleEnum.ITALIC)} />
                <button className="toggle-underline" onClick={styleButton(StyleEnum.UNDER)} />
                <ColorPicker setColor={(color)=>setStyle({...style,color:color})}/>
            </div>
            <button onClick={props.onSendMessage(content,style)}>Send</button>
        </div>
    );
}

export default MessageInput
