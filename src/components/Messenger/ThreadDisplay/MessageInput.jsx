import React, { useState } from "react";
import { connect } from "react-redux";

import {
  StyleEnum,
  textStyles,
  colorFromInt
} from "../../../utils/text-styling";

const ColorPicker = props => {
  const N_COLORS = 8;
  let colorOptions = [...Array(N_COLORS).keys()].map(ind => {
    const colorString = colorFromInt(ind, N_COLORS);
    return (
      <option
        value={colorString}
        style={{ color: colorString }}
        key={"colorpicker." + colorString}
      >
        ■
      </option>
    );
  });
  const [selected, setSelected] = useState(colorOptions[0].value);
  return (
    <select
      className="text-color-picker"
      onChange={e => {
        props.setColor(e.target.value);
        setSelected(e.target.value);
      }}
      style={{ color: selected }}
      value={selected}
    >
      {colorOptions}
    </select>
  );
};

// Needs props:
// --onSendMessage: func(content,style)
const MessageInput = props => {
  const MAX_CHARS = 10;
  const [content, setContent] = useState("");
  const [style, setStyle] = useState({ ...textStyles(0), color: "#000" });

  const styleButton = styleType => () =>
    setStyle({ ...style, text: StyleEnum.toggleStyle(style, styleType) });
  return (
    <div>
      <div className="input-container">
        <textarea
          className="message-text-input"
          rows={4}
          cols={60}
          style={style}
          maxLength={MAX_CHARS}
          onInput={e => {
            console.log(e.target.value);
            console.log("content", content);
            if (e.target.value <= MAX_CHARS) {
            }
            setContent(e.target.value);
          }}
        />
      </div>
      <div>
        <button
          className="toggle-bold"
          onClick={e => styleButton(StyleEnum.BOLD)}
        />
        <button
          className="toggle-italic"
          onClick={e => styleButton(StyleEnum.ITALIC)}
        />
        <button
          className="toggle-underline"
          onClick={e => styleButton(StyleEnum.UNDER)}
        />
        <ColorPicker setColor={color => setStyle({ ...style, color: color })} />
      </div>
      <button onClick={props.onSendMessage(content, style)}>Send</button>
    </div>
  );
};

export default MessageInput;
