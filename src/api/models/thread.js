export default class Thread {
  constructor(id, name, members, messages, created) {
    this.id = id;
    this.name = name ? name : "";
    this.members = members ? members : [];
    this.messages = messages ? messages : [];
    this.created = created;
  }
}
