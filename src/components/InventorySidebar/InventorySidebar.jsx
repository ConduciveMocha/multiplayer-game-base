import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import "./InventorySidebar.css";

const NO_ITEM_ID = -1;

const InventoryItem = ({ item, selected, onClickHandler }) => {
  return (
    <div
      onClick={() => onClickHandler()}
      className={selected ? "inventory-item-selected" : "inventory-item"}
    >
      <h2 className={"inventory-item-name"}>{item.name}</h2>
      <h3>x{item.quantity}</h3>
    </div>
  );
};

const InventorySidebar = props => {
  const [selectedItemId, setSelectedItemId] = useState(NO_ITEM_ID);

  const inventoryItems = Object.keys(props.inventory).map(itemId => {
    const item = props.inventory[parseInt(itemId)];
    return (
      <InventoryItem
        key={"inventory-item-" + item.id}
        item={item}
        selected={selectedItemId === item.id}
        onClickHandler={() => {
          setSelectedItemId(item.id);
        }}
      />
    );
  });

  return (
    <div
      className="inventory-sidebar"
      onBlur={() => {
        setSelectedItemId(NO_ITEM_ID);
      }}
    >
      <h1 className="inventory-header">Inventory</h1>
      <div className="inventory-items-container">{inventoryItems}</div>
    </div>
  );
};

export default connect(
  state => ({ inventory: state.game.inventory }),
  dispatch => ({})
)(InventorySidebar);
