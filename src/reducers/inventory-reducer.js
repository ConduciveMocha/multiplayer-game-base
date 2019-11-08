import { inventoryMock } from "../utils/game-mock";
import * as inventoryTypes from "../constants/action-types/inventory-types";

const initialInventoryState = inventoryMock;
export default function inventoryReducer(
  state = initialInventoryState,
  action
) {
  switch (action.type) {
    case inventoryTypes.LOAD_USER_OBJECTS:
      return { ...action.userInventory };
    case inventoryTypes.ACQUIRE_ITEM_CONFIRMED:
      return { ...state, [action.item.itemId]: action.item };

    case inventoryTypes.ACQUIRE_ITEM_ERROR:
    case inventoryTypes.DELETE_ITEM_CONFIRMED:
    case inventoryTypes.DELETE_ITEM_ERROR:
    case inventoryTypes.DROP_ITEM_CONFIRMED:
    case inventoryTypes.DROP_ITEM_ERROR:

    default:
      console.log("Action from inventoryReducer", action);
  }
}
