import * as inventoryTypes from "../constants/action-types/inventory-types";

export const sendAcquireItem = itemId => ({
  type: inventoryTypes.ACQUIRE_ITEM,
  itemId: itemId
});

export const sendDropItem = itemId => {
  console.log("sendDropItem called");
  return {
    type: inventoryTypes.DROP_ITEM,
    itemId: itemId
  };
};

export const sendDeleteItem = itemId => ({
  type: inventoryTypes.DELETE_ITEM,
  itemId: itemId
});

export const acquireItemConfirmed = itemId => ({
  type: inventoryTypes.ACQUIRE_ITEM_CONFIRMED,
  itemId
});

export const dropItemConfirmed = itemId => ({
  type: inventoryTypes.DROP_ITEM_CONFIRMED,
  itemId
});

export const deleteItemConfirmed = itemId => ({
  type: inventoryTypes.DELETE_ITEM_CONFIRMED,
  itemId
});

export const acquireItemError = (itemId, errorMessage) => ({
  type: inventoryTypes.ACQUIRE_ITEM_ERROR,
  itemId,
  errorMessage
});

export const dropItemError = (itemId, errorMessage) => ({
  type: inventoryTypes.DROP_ITEM_ERROR,
  itemId,
  errorMessage
});

export const deleteItemError = (itemId, errorMessage) => ({
  type: inventoryTypes.DELETE_ITEM_ERROR,
  itemId,
  errorMessage
});
