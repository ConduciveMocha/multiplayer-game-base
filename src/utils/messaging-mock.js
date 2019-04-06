/**
 * Message = {
 *              sender_id: int
 *              thread_id: int
 *              message: string
 *              timestamp: date
 *              recieved: bool
 *              read: bool
 * }
 * Thread = {
 *              members: [int]
 *              thread_id: [int]
 *              messages: [Message]
 *              hasNew: bool
 *              textBoxState: string
 * }
 * 
 * MessageStore = {
 *              threads: [Thread]
 *              visibleThreads: [Threads]
 *              currentThread: Thread
 *              onlineUsers: [user_ids]
 * }
 * 
 * 
 * Flow:
 *      1. Global Feed Defaults to Open
 *      2. Message  
 * 
 */


export const mockUsers = [1,2, 3, 4, 5, 6, 7, 8, 9, 10].map(x => 20 + x);
export const GLOBAL_THREAD_ID = 0;
export const mockThreads = [
    {
        threadId:1,
        active: false,
        unread:true,
        members:mockUsers,
        messages:[
            {
                messageId:1,
                senderId: mockUsers[0],
                threadId:1,
                message:"HelloWorld",
                timestamp:new Date().getTime()
            },
            {
                messageId: 2,
                senderId: mockUsers[1],
                threadId: 1,
                message: "Bonjour",
                timestamp: new Date().getTime()
            },
            {
                messageId: 3,
                senderId: mockUsers[0],
                threadId: 1,
                message: "Hello France!",
                timestamp: new Date().getTime()
            },

        ]
    },
    {
        threadId:2,
        active:true,
        unread:false,
        members:mockUsers.slice(3),
        messages:[
            {
                messageId:4,
                senderId: mockUsers[4],
                threadId:2,
                content:"Other thread",
                timestamp:new Date().getTime()
            },
            {
                messageId: 5,
                senderId: mockUsers[5],
                threadId: 2,
                content: "Indeed",
                timestamp: new Date().getTime()
            }
        ]
    }
]