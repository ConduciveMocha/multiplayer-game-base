import React from "react";
import useBool from "../../../hooks/useBool";
const CollapsableList = ({ ListItemComponent, proplist, listName }) => {
  const toggler = useBool(true);
  let listItems = proplist.map(props => {
    return <ListItemComponent {...props} />;
  });
  return (
    <div className="collapsable-list-container">
      <div
        className="collapsable-list-title"
        onClick={e => {
          toggler.toggle();
        }}
      >
        <div
          className={
            toggler.value ? "collapse-icon-shown" : "collapse-icon-hidden"
          }
        />
        <span>{listName}</span>
      </div>
      <div className="collapsable-list-items">
        {toggler.value ? listItems : []}
      </div>
    </div>
  );
};

export default CollapsableList;
