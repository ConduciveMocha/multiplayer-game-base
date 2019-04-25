// TODO: Merge this with the model code
export const makeThreadId = members => {
  members.sort((a, b) => a - b);
  let enc = String(members[0]);
  for (let i = 1; i < members.length; i++) {
    enc += "_" + String(members[i] - members[i - 1]);
  }
  return btoa(enc);
};

export const membersFromThreadId = threadId => {
  let dec = atob(threadId);
  let members = dec.split("_").map(el => parseInt(el, 10));

  for (let i = 1; i < membbers.length; i++) {
    members[i] += members[i - 1];
  }

  return members;
};
