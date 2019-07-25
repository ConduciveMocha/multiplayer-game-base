export default class ModelBase {
  constructor(storeFields) {
    this.storeFields = storeFields;
  }

  getStoreObject() {
    let storeObj = {};
    for (let i = 0; i < this.storeFields.length; i++) {
      storeObj[this.storeFields[i]] = this[this.storeFields[i]];
    }
    return { ...storeObj };
  }
}
