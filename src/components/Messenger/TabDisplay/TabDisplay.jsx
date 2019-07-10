import React from "react";
import TabContainer from "./TabContainer";
import MessageContainer from "./MessageContainer";
import InputContainer from "./InputContainer";

const TabDisplay = props => {
  return (
    <div>
      <TabContainer />
      <MessageContainer />
      <InputContainer />
    </div>
  );
};

export default TabDisplay;
