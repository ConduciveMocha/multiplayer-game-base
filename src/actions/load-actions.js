import {
  THREADS_LOADED,
  THREAD_MESSAGES_LOADED,
  USERS_LOADED
} from "../constants/action-types/message-types";

export const threadsLoaded = threads => ({
  type: THREADS_LOADED,
  threads: threads
});

export const usersLoaded = usersList => {
  console.log(usersList);
  return {
    type: USERS_LOADED,
    online: usersList.online,
    friends: usersList.friends
  };
};

export const threadMessagesLoaded = messages => ({
  type: THREAD_MESSAGES_LOADED,
  messages: messages
});
