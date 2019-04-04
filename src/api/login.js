import {withJwt, jsonPost} from './index'


export const submitLogin = (username,password) => withJwt(jsonPost)({username:username,password:password},'/auth/login');
