import * as inventoryTypes from "../constants/action-types/inventory-types";

export const sendDropItem = itemId => ({
  type: inventoryTypes.DROP_ITEM,
  itemId: itemId
});

export const sendDeleteItem = itemId => ({
  type: inventoryTypes.DELETE_ITEM,
  itemId: itemId
});
