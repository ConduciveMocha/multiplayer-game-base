import React, {useState,useEffect} from 'react';
import NO_ERROR from '../../constants/NoError'
import useValidator from './useValidator'; 

// Custom hook for managing an input field
const useInputField = (initialState, validator,sendState) => {
    const {fieldValue, fieldErrors,isValid,fieldChange} = useValidator(initialState,validator);
    const [error, setError] = useState(fieldErrors ? fieldErrors[0] : NO_ERROR);

    useEffect(()=>{
        setError(fieldErrors ? fieldErrors[0] : NO_ERROR);
    },[fieldErrors])
    
    const onChange = e => {fieldChange(e.target.value)};
    const onBlur = () => {isValid ? sendState(fieldValue) : sendState(null);}


    return {onChange,onBlur,error};
}

export default useInputField;