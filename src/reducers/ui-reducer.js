import * as AuthTypes from '../constants/action-types/auth-types'
import * as LoadTypes from '../constants/action-types/load-types'
//import FocusStates from '../constants/FocusStates'
import NO_ERROR from '../constants/NoError'
const uiInitialState = {
    currentFocus:null, 
    showComponents:{
        loginScreen:true,
        registrationScreen:false,
        gameScreen:false,
        loadingScreen:false
    },
    visibleErrors:[NO_ERROR]
};

export default function uiReducer(state=uiInitialState, action) {
    switch(action.type) {
        case AuthTypes.LOGIN_SUCCESS:
            return {...state, showComponents:{...state.showComponents, loginScreen:false,loadingScreen:true}}
     
        case AuthTypes.LOGIN_FAILED:
            return {...state,visibleErrors:[...state.visibleErrors,action.error]}

        case LoadTypes.INITIAL_LOAD_FINISHED:
            return {...state,showComponents:{...state.showComponents,loadingScreen:false,gameScreen:true}}

        default:
            return state;
    }
}