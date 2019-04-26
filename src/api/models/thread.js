export default class Thread {
  constructor(id, name, members, messages, created) {
    this.id = id;
    this.initialized = this.id !== -1;
    this.threadHash = threadHash;
    this.name = name ? name : "";
    this.members = members ? members : [];
    this.messages = messages ? messages : [];
    this.created = created;
    this.savedAddedUsersList = [];
  }

  static makeThreadHash(members) {
    if (typeof members === Object) {
      members = members.map(mem => mem.id);
    }
    members.sort((a, b) => a - b);
    let enc = String(members[0]);
    for (let i = 1; i < members.length; i++) {
      enc += "_" + String(members[i] - members[i - 1]);
    }
    return btoa(enc);
  }

  static memberIdsFromThreadHasH(threadHash) {
    let dec = atob(threadHash);
    let members = dec.split("_").map(el => parseInt(el, 10));

    for (let i = 1; i < members.length; i++) {
      members[i] += members[i - 1];
    }

    return members;
  }

  setMembers(members) {
    this.members = [...members];
    this.threadHash = this.makeThreadHash(this.members);
  }
}
