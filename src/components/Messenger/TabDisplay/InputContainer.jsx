import React from "react";

const InputContainer = props => {
  return (
    <div className="input-container">
      <textarea rows="4" cols="125" onChange={e => props.onChangeFtn(e)} />
      <button>Send</button>5
    </div>
  );
};

export default InputContainer;
