import React from "react";

const InputContainer = ({ inputContent, onChangeFtn, sendFtn }) => {
  return (
    <div className="input-container">
      <textarea rows="4" cols="125" onChange={e => onChangeFtn(e)} value={inputContent} onKeyPress={(e)=>{if (e.key==='Enter'){sendFtn(inputContent)}}} />
      <button
        onClick={() => {
          sendFtn(inputContent);
        }}
      >
        Send
      </button>
    </div>
  );
};

export default InputContainer;
