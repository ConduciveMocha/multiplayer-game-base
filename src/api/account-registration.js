import {flaskServer} from './urls'
import {jsonPost} from './index'

export const submitRegistration = (registrationFrom) => jsonPost(registrationFrom)
